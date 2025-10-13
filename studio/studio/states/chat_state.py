import asyncio
import base64
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
from veadk.utils.misc import formatted_timestamp

from studio.states import agent_state
from studio.states.agent_state import AgentState
from studio.types import Message
from studio.utils.misc import extract_mime_type, image_base64_to_bytes, image_to_base64

logger = get_logger(__name__)


def event_to_messages(event: Event) -> Message | list[Message] | None:
    if event.author == "user":
        if event.content and event.content.parts:
            _messages: list[Message] = []
            for part in event.content.parts:
                if part.text:
                    _messages.append(Message(role="user", content=part.text))
                if (
                    part.inline_data
                    and part.inline_data.data
                    and part.inline_data.mime_type
                ):
                    image_bytes = part.inline_data.data
                    image_base64_str = f"data:{part.inline_data.mime_type};base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    _messages.append(Message(role="user", image=image_base64_str))
            return _messages

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


async def update_session_attrs(state: rx.State):
    session_state = await state.get_state(SessionState)
    eval_state = await state.get_state(EvalState)

    await session_state.update_session_events_count_map()
    await session_state.update_session_last_update_time_map()

    await eval_state.update_eval_cases()


class SessionState(rx.State):
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

        await self._update_states()

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
    async def save_session(self):
        pass

        # yield rx.toast(...)

    @rx.event
    async def update_session_events_count_map(self):
        logger.debug("Update session events count map.")

        assert (
            agent_state.runner and agent_state.runner.short_term_memory is not None
        ), "Runner or short term memory is not initialized."
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

        assert (
            agent_state.runner and agent_state.runner.short_term_memory is not None
        ), "Runner or short term memory is not initialized."
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

    async def _update_states(self) -> None:
        # Step 1: update message list
        session = self.session
        message_state = await self.get_state(MessageState)
        message_state.load_message_list(session)

        # Step 2: update session attributes
        await self.update_session_events_count_map()
        await self.update_session_last_update_time_map()

        # Step 3: update eval cases
        eval_state = await self.get_state(EvalState)
        await eval_state.update_eval_cases()


class MessageState(rx.State):
    user_message_text: str = ""
    """User's latest message text. We donot direcrly use `prompt` because the user interface cannot render user message imediately after user click send button."""

    user_message_text_draft: str
    """Temporary prompt storage for input box value binding. After user click send button, the prompt will be moved to `user_message_text`."""

    user_message_images: list[str] = []
    """User's latest message images (file names)"""

    user_message_images_draft: list[str] = []
    """User's latest message images preview in user's input box. The data is base64 encoded string."""

    processing: bool = False
    """Whether processing user's prompt"""

    message_list: list[Message]
    """History message list in current session"""

    @rx.event
    def set_user_message(self):
        self.message_list.append(
            Message(role="user", content=self.user_message_text_draft)
        )
        self.user_message_text = self.user_message_text_draft

        for prompt_image in self.user_message_images_draft:
            self.user_message_images.append(prompt_image)

            self.message_list.append(Message(role="user", image=prompt_image))

        # clear draft data
        self.user_message_text_draft = ""
        self.user_message_images_draft = []

    @rx.event
    async def set_user_message_images_draft(self, files: list[rx.UploadFile]):
        for file in files:
            data = await file.read()
            if file.name:
                base64_str = image_to_base64(filename=file.name, data=data)
                self.user_message_images_draft.append(base64_str)

    @rx.event
    def load_message_list(self, session: Session):
        _message_list: list[Message] = []
        for event in session.events:
            message = event_to_messages(event)
            if message:
                _message_list.append(message) if isinstance(
                    message, Message
                ) else _message_list.extend(message)
        self.message_list = _message_list

    @rx.event
    async def generate(self):
        """Handle user task request.

        We need to process the following message:
        - User message:
          - Text
          - Image
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

        session_state = await self.get_state(SessionState)
        user_id = session_state.session.user_id
        session_id = session_state.session.id

        logger.debug(
            f"Begin generate, app_name: {agent_state.runner.app_name}, user_id: {user_id}, session_id: {session_id}"
        )

        # Build user message parts
        # 1. Text part
        user_parts = [Part(text=self.user_message_text)]
        # 2. Image parts if any
        for image_base64_str in self.user_message_images:
            user_parts.append(
                Part(
                    inline_data=Blob(
                        data=image_base64_to_bytes(image_base64_str),
                        mime_type=extract_mime_type(image_base64_str),
                    )
                )
            )
        # 3. Build content
        new_message = Content(parts=user_parts, role="user")

        try:
            async for event in agent_state.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=new_message,
            ):
                message = event_to_messages(event)
                if message:
                    self.message_list.append(message) if isinstance(
                        message, Message
                    ) else self.message_list.extend(message)
                    yield
        except Exception as e:
            message = Message(role="assistant", content=str(e))
            yield

        self._clear_user_input_message()
        await self._update_states()

        self.processing = False

        logger.debug("Generate done.")

    def _clear_user_input_message(self) -> None:
        self.user_message_text = ""
        self.user_message_images = []

    async def _update_states(self) -> None:
        session_state = await self.get_state(SessionState)
        await session_state.update_session_events_count_map()
        await session_state.update_session_last_update_time_map()

        eval_state = await self.get_state(EvalState)
        await eval_state.update_eval_cases()


class EvalState(rx.State):
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

    evaluating: bool = False

    judge_score: str = ""

    judge_reason: str = ""

    @rx.event
    async def update_eval_cases(self):
        logger.debug("Update eval cases.")

        session_state = await self.get_state(SessionState)
        app_name = session_state.app_name
        user_id = session_state.user_id
        session_id = session_state.session_id

        assert (
            agent_state.runner and agent_state.runner.short_term_memory is not None
        ), "Runner or short term memory is not initialized."
        session = await get_session(
            app_name,
            user_id,
            session_id,
            agent_state.runner.short_term_memory,
        )

        logger.debug(f"Update eval case with session id {session.id}")

        self.eval_cases = evals.convert_session_to_eval_invocations(session)

        self.eval_cases_map = {
            eval_case.invocation_id: eval_case for eval_case in self.eval_cases
        }

    @rx.event
    async def evaluate(self, eval_case_id: str):
        logger.debug("Start to evaluate.")

        self.evaluating = True
        yield

        invocation = self.eval_cases_map.get(eval_case_id)
        if not invocation:
            logger.error(f"Get eval case failed (eval_case_id={eval_case_id})")

        logger.debug("Start to prepare evaluation set.")

        session_state = await self.get_state(SessionState)
        app_name = session_state.app_name
        user_id = session_state.user_id

        _eval_case = ADKEvalCase(
            eval_id=f"eval_{formatted_timestamp()}",
            conversation=[invocation],  # type: ignore
            session_input=SessionInput(
                app_name=app_name,
                user_id=user_id,
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

        self.evaluating = False
        yield
