import asyncio
import os
import uuid
from datetime import datetime

import reflex as rx
from deepeval.metrics import GEval, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCaseParams
from google.adk.cli.utils import evals
from google.adk.evaluation.eval_case import EvalCase as ADKEvalCase
from google.adk.evaluation.eval_case import Invocation, SessionInput
from google.adk.evaluation.eval_set import EvalSet as ADKEvalSet
from google.adk.events import Event
from google.adk.sessions import Session
from google.genai.types import Blob, Content, Part
from veadk.evaluation.deepeval_evaluator.deepeval_evaluator import DeepevalEvaluator
from veadk.memory import ShortTermMemory
from veadk.utils.logger import get_logger
from veadk.utils.misc import formatted_timestamp, read_png_to_bytes

from studio.states import agent_state
from studio.states.agent_state import AgentState
from studio.types import Message

logger = get_logger(__name__)


def event_to_message(event: Event) -> Message | None:
    if event.author == "user":
        return Message(role="user", content=event.content.parts[0].text)  # type: ignore

    if event.get_function_calls():
        for function_call in event.get_function_calls():
            return Message(
                role="tool_call",
                tool_name=function_call.name
                if function_call.name
                else "<unknown_tool_name>",
                tool_args=str(function_call.args),
                event_id=event.id,
            )

    if event.get_function_responses():
        for function_response in event.get_function_responses():
            return Message(
                role="tool_response",
                tool_name=function_response.name
                if function_response.name
                else "<unknown_tool_name>",
                tool_response=str(function_response.response),
                event_id=event.id,
            )

    if (
        not event.partial
        and event.content is not None
        and event.content.parts
        and event.content.parts[0].text is not None
        and len(event.content.parts[0].text.strip()) > 0
    ):
        final_response = event.content.parts[0].text
        return Message(
            role="assistant",
            content=final_response,
            event_id=event.id,
            invocation_id=event.invocation_id,
        )


async def get_session(
    app_name: str, user_id: str, session_id: str, short_term_memory: ShortTermMemory
) -> Session:
    session_service = short_term_memory.session_service

    session = await session_service.get_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    if not session:
        raise RuntimeError("Session not found.")

    return session


class MessageState(rx.State):
    """
    States for session management
    """

    app_name: str
    """One of Google ADK attributes"""

    user_id: str = "user_" + str(uuid.uuid4()).split("-")[0]
    """One of Google ADK attributes"""

    session_id: str
    """One of Google ADK attributes"""

    session: Session
    """Current activated session."""

    session_events_count_map: dict[str, int] = {}
    """Map from session id to number of events in the session"""

    session_last_update_time_map: dict[str, str] = {}
    """Map from session id to timestamp of the last update time of the session"""

    sessions: list[Session] = []
    """All sessions for current app and user"""

    event_content: str = "No event selected."
    """The currently selected event content"""

    """
    States for message management
    """

    prompt: str
    """User's latest prompt"""

    prompt_images: list[str] = []
    """User's latest prompt images (file names)"""

    processing: bool = False
    """Whether processing user's prompt"""

    message_list: list[Message]
    """History message list in current session"""

    """
    States for evaluation
    """

    eval_cases: list[Invocation] = []
    """Invocations of the Google ADK Evalcase.

    Structure:
    - ADKEvalset
        - eval_cases: list[ADKEvalcase]
            - conversation: list[Invocation] --> eval_cases here
    """

    eval_cases_map: dict[str, Invocation] = {}
    """Map from invocation id to invocation"""

    judge_model_name: str = "doubao-seed-1-6-250615"

    judge_model_prompt: str = "You are a judger for model response."

    judge_score: str = ""

    judge_reason: str = ""

    """
    Methods for session management
    """

    @rx.event
    async def add_session(self):
        """Add a session to current (app_name, user_id)"""
        new_session_id = str(uuid.uuid4()).split("-")[0]

        agent_state = await self.get_state(AgentState)

        session = await agent_state.short_term_memory.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=new_session_id,
        )

        if session:
            self.session_id = session.id
            self.session = session
            self.sessions.append(session)

            logger.debug(f"Create session with id {session.id}")

            # imediately load the new-created session
            await self.load_session(session.id)
        else:
            logger.error("Create session failed, please check veadk-python logs.")

    @rx.event
    async def load_session(self, session_id: str):
        session = await get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=session_id,
            short_term_memory=(await self.get_state(AgentState)).short_term_memory,
        )
        self.session = session
        self.session_id = session.id

        logger.info(f"Get session with session_id={session.id}")
        logger.info(f"Session has {len(session.events)} events")

        # Step 1: update message list
        message_state = await self.get_state(MessageState)
        message_state.load_message_list(session)

        # Step 2: update session to num events map & timestamp map
        await self.update_session_events_count_map()
        await self.update_session_last_update_time_map()

        # Step 3: update eval cases
        await self.update_eval_cases()

    @rx.event
    def load_event(self, event_id: str):
        logger.debug(
            f"Load event {event_id} in app_name={self.app_name}, user_id={self.user_id}, session {self.session.id} ({len(self.session.events)} events)"
        )
        for event in self.session.events:
            if event.id == event_id:
                self.event_content = event.model_dump_json(indent=2)
                break

    @rx.event
    async def load_sessions(self):
        agent_state = await self.get_state(AgentState)

        if agent_state.short_term_memory:
            session_service = agent_state.short_term_memory.session_service

            list_sessions_response = await session_service.list_sessions(
                app_name=self.app_name, user_id=self.user_id
            )
            self.sessions = list_sessions_response.sessions
        else:
            self.sessions = []

    @rx.event
    async def update_session_events_count_map(self):
        logger.debug("Update session events count map.")

        session = await get_session(
            self.app_name,
            self.user_id,
            self.session_id,
            agent_state.runner.short_term_memory,
        )
        self.session = session

        self.session_events_count_map[self.session.id] = len(self.session.events)

    @rx.event
    async def update_session_last_update_time_map(self):
        logger.debug("Update session last update time map.")

        session = await get_session(
            self.app_name,
            self.user_id,
            self.session_id,
            agent_state.runner.short_term_memory,
        )
        self.session = session

        self.session_last_update_time_map[self.session.id] = datetime.fromtimestamp(
            self.session.last_update_time
        ).strftime("%Y-%m-%d %H:%M:%S")

    @rx.var
    def reversed_sessions(self) -> list[Session]:
        return list(reversed(self.sessions))

    @rx.var
    def num_sessions(self) -> int:
        return len(self.sessions)

    """
    Methods for message management
    """

    @rx.event
    def set_user_message(self):
        self.message_list.append(Message(role="user", content=self.prompt))

        for prompt_image in self.prompt_images:
            self.message_list.append(Message(role="user", image=prompt_image))

    @rx.event
    async def set_user_images(self, files: list[rx.UploadFile]):
        for file in files:
            data = await file.read()
            if file.name:
                path = rx.get_upload_dir() / file.name
                with path.open("wb") as f:
                    f.write(data)
                logger.debug(f"Save uploaded file to {str(path.absolute())}")
                self.prompt_images.append(file.name)

    @rx.event
    def load_message_list(self, session: Session):
        _message_list: list[Message] = []
        for event in session.events:
            message = event_to_message(event)
            if message:
                _message_list.append(message)
        self.message_list = _message_list

    @rx.event
    async def generate(self):
        """Handle user task request.

        We need to process the following message:
        - User message:
          - Text
          - TODO(yaozheng): Image
        - Agent message:
          - Text
          - Function call
          - Function response
              - Text
              - Image
        """
        assert agent_state.runner is not None, "Runner is not initialized."

        self.processing = True
        yield

        logger.debug(
            f"Begin generate, app_name: {agent_state.runner.app_name}, user_id: {self.user_id}, session_id: {self.session_id}"
        )

        user_parts = [Part(text=self.prompt)]
        for image_path in self.prompt_images:
            image_data = read_png_to_bytes(str(rx.get_upload_dir() / image_path))
            if image_data:
                user_parts.append(
                    Part(inline_data=Blob(data=image_data, mime_type="image/png"))
                )
            os.remove(str(rx.get_upload_dir() / image_path))
        new_message = Content(parts=user_parts, role="user")

        try:
            async for event in agent_state.runner.run_async(  # type: ignore
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=new_message,
            ):
                message = event_to_message(event)
                if message:
                    self.message_list.append(message)
                    yield
        except Exception as e:
            message = Message(role="assistant", content=str(e))
            yield

        self.prompt = ""

        await self.update_session_events_count_map()
        await self.update_session_last_update_time_map()

        await self.update_eval_cases()

        self.processing = False

        logger.debug("Generate done.")

    """
    Methods for evaluation
    """

    @rx.event
    async def update_eval_cases(self):
        session = await get_session(
            self.app_name,
            self.user_id,
            self.session_id,
            agent_state.runner.short_term_memory,
        )
        self.session = session

        logger.debug(f"Update eval case with session id {session.id}")

        self.eval_cases = evals.convert_session_to_eval_invocations(session)

        self.eval_cases_map = {
            eval_case.invocation_id: eval_case for eval_case in self.eval_cases
        }

    @rx.event
    async def evaluate(self, eval_case_id: str):
        logger.debug("Start to evaluate.")

        invocation = self.eval_cases_map.get(eval_case_id)
        if not invocation:
            logger.error(f"Get eval case failed (eval_case_id={eval_case_id})")

        logger.debug("Start to prepare evaluation set.")

        _eval_case = ADKEvalCase(
            eval_id=f"eval_{formatted_timestamp()}",
            conversation=[invocation],  # type: ignore
            session_input=SessionInput(
                app_name=self.app_name,
                user_id=self.user_id,
                state={},
            ),
            creation_timestamp=0.0,
        )

        logger.debug("Prepare evaluation case done.")

        _eval_set = ADKEvalSet(
            eval_set_id=f"eval_{formatted_timestamp()}",
            eval_cases=[_eval_case],
            creation_timestamp=0.0,
        )

        logger.debug("Prepare evaluation set done.")

        agent_state = await self.get_state(AgentState)
        agent = agent_state.agent
        evaluator = DeepevalEvaluator(agent=agent)

        logger.debug("Prepare evaluator done.")

        metrics = [
            GEval(
                threshold=0.8,
                name="Base Evaluation",
                criteria=self.judge_model_prompt,
                evaluation_params=[
                    LLMTestCaseParams.INPUT,
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                    LLMTestCaseParams.EXPECTED_OUTPUT,
                ],
                model=evaluator.judge_model,
            ),
            ToolCorrectnessMetric(threshold=0.5),
        ]

        logger.debug("Prepare metrics done.")

        def run_in_new_loop():
            return asyncio.run(evaluator.evaluate(metrics=metrics, eval_set=_eval_set))

        import concurrent.futures

        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, run_in_new_loop)

        # await evaluator.evaluate(metrics=metrics, eval_set=_eval_set)

        self.judge_score = str(evaluator.result_list[0].average_score)
        self.judge_reason = evaluator.result_list[0].total_reason
