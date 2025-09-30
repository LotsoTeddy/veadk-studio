import time
import uuid
from pathlib import Path

import reflex as rx
from google.adk.agents import Agent
from google.adk.cli.utils import evals
from google.adk.cli.utils.agent_loader import AgentLoader
from google.adk.evaluation.eval_case import EvalCase as ADKEvalCase
from google.adk.evaluation.eval_case import Invocation, SessionInput
from google.adk.evaluation.eval_set import EvalSet as ADKEvalSet
from google.adk.events import Event
from google.genai.types import Content, Part
from veadk import Runner
from veadk.evaluation.deepeval_evaluator.deepeval_evaluator import DeepevalEvaluator
from veadk.utils.logger import get_logger
from veadk.utils.misc import formatted_timestamp

from studio.types import EvalCase, Message

logger = get_logger(__name__)

agent_loader = AgentLoader(agents_dir=str(Path.cwd()))

runner: Runner | None = None


class AgentState(rx.State):
    agent: Agent
    """Global agent instance"""

    selected_agent: str = ""
    """The current selected agent name"""

    @rx.var
    def list_agents(self) -> list[str]:
        """List agent from current work directory"""
        return agent_loader.list_agents()

    @rx.event
    def set_agent(self, agent_name: str):
        """Set the user-selected agent and init a runner.

        Args:
            agent_name: selected agent directory name
        """
        # set agent name and load agent to memory
        self.selected_agent = agent_name

        agent = agent_loader.load_agent(agent_name)
        assert isinstance(agent, Agent), (
            f"Only support Agent type, but got {agent.__class__.__name__}"
        )
        self.agent = agent

        # init runner
        global runner
        runner = Runner(agent=self.agent)

        # redirect to session page
        return rx.redirect("/agent")

    @rx.event
    def update_system_prompt(self, prompt: str):
        self.agent.instruction = prompt


class ChatState(rx.State):
    app_name: str = "veadk_studio"
    """One of Google ADK attributes"""

    user_id: str = f"u_{uuid.uuid4()}"
    """One of Google ADK attributes"""

    session_id: str = f"s_{uuid.uuid4()}"
    """One of Google ADK attributes"""

    session_ids: list[str] = []
    """Maintain a list of session ids for rendering in the session tab"""

    selected_event_content: str = ""
    """The currently selected event content"""

    prompt: str
    """User's latest prompt"""

    processing: bool = False
    """Whether processing user's prompt"""

    message_list: list[Message]
    """History message list in current session"""

    eval_cases: list[Invocation] = []
    """Inovcations of the Google ADK Evalcase.
    
    Structure:
    - ADKEvalset
        - eval_cases: list[ADKEvalcase]
            - conversation: list[Invocation] --> eval_cases here
    """

    # chat services
    @rx.event
    def set_app_name(self, app_name: str):
        self.app_name = app_name

    @rx.event
    def set_prompt(self, prompt: str):
        self.prompt = prompt
        self.message_list.append(Message(role="user", content=self.prompt))

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
        new_message = Content(parts=[Part(text=self.prompt)], role="user")

        self.processing = True
        yield

        async for event in runner.run_async(  # type: ignore
            user_id=self.user_id,
            session_id=self.session_id,
            new_message=new_message,
        ):
            message = self._event_to_message(event)
            if message:
                self.message_list.append(message)
                yield

        await self.update_eval_case()

        self.prompt = ""

        self.processing = False

    # evaluation services
    async def update_eval_case(self):
        if runner and runner.short_term_memory:
            session_service = runner.short_term_memory.session_service

            session = await session_service.get_session(
                app_name=self.app_name, user_id=self.user_id, session_id=self.session_id
            )

            if not session:
                logger.error("Session not found, update eval case failed.")
                return

            # Convert the session data to eval invocations
            self.eval_cases = evals.convert_session_to_eval_invocations(session)

    @rx.event
    def evaluate_eval_case(self):
        # evaluator = DeepevalEvaluator(agent=self.agent)
        # eval_set = ADKEvalSet(
        #     eval_set_id=formatted_timestamp(), eval_cases=self.eval_cases
        # )
        # evaluator.evaluate(eval_set=eval_set)
        pass

    # session services
    @rx.event
    async def get_event(self, event_id: str):
        if runner and runner.short_term_memory:
            session_service = runner.short_term_memory.session_service

            logger.info(f"Load session with expected session_id={self.session_id}")
            session = await session_service.get_session(
                app_name=self.app_name, user_id=self.user_id, session_id=self.session_id
            )
            if session:
                logger.info(f"Get session with session_id={session.id}")
                logger.info(f"Session has {len(session.events)} events")

                for event in session.events:
                    if event.id == event_id:
                        self.selected_event_content = event.model_dump_json(indent=2)
            else:
                logger.warning("No history events found in session.")

    @rx.event
    async def update_runner_config_from_form(self, data: dict | None = None):
        if data:
            app_name = data["app_name"]
            user_id = data["user_id"]
            session_id = data["session_id"]

            self.app_name = app_name
            self.user_id = user_id
            self.session_id = session_id

            global runner
            if runner and runner.short_term_memory:
                await runner.short_term_memory.create_session(
                    app_name=self.app_name,
                    user_id=self.user_id,
                    session_id=session_id,
                )
                self.session_ids.append(session_id)

            if runner:
                runner.app_name = self.app_name
                runner.user_id = self.user_id
        else:
            logger.error("Receive no form data!")

    @rx.event
    async def add_session(self):
        session_id = f"s_{uuid.uuid4()}"

        if runner and runner.short_term_memory:
            await runner.short_term_memory.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=session_id,
            )
            self.session_ids.append(session_id)
            self.session_id = session_id

    @rx.event
    async def load_sessions(self):
        if runner and runner.short_term_memory:
            session_service = runner.short_term_memory.session_service

            list_sessions_response = await session_service.list_sessions(
                app_name=self.app_name, user_id=self.user_id
            )
            sessions = list_sessions_response.sessions
            self.session_ids = [session.id for session in sessions]
        else:
            self.session_ids = []

    @rx.event
    async def load_session(self, session_id: str):
        """Load session from a session service, and set the history conversations to chat state."""
        if runner and runner.short_term_memory:
            session_service = runner.short_term_memory.session_service

            logger.info(f"Load session with expected session_id={session_id}")
            session = await session_service.get_session(
                app_name=self.app_name, user_id=self.user_id, session_id=session_id
            )
            if session:
                logger.info(f"Get session with session_id={session.id}")
                logger.info(f"Session has {len(session.events)} events")

                _message_list: list[Message] = []
                for event in session.events:
                    message = self._event_to_message(event)
                    if message:
                        _message_list.append(message)
                self.message_list = _message_list

            else:
                logger.warning("No history events found in session.")

    def _event_to_message(self, event: Event) -> Message | None:
        if event.get_function_calls():
            for function_call in event.get_function_calls():
                logger.debug(f"Function call: {function_call}")
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
                logger.debug(f"Function response: {function_response}")
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

            return Message(role="assistant", content=final_response, event_id=event.id)

    # control services
    # async def handle_key_down(self, key: str):
    #     if key == "Enter":
    #         async for t in self.answer():
    #             yield t


class PageState(rx.State):
    open_settings_dialog_flag: bool = False
    open_prompt_optimize_dialog_flag: bool = False
    deploy_dialog_flag: bool = False

    # settings dialog
    @rx.event
    def open_settings_dialog(self):
        self.open_settings_dialog_flag = True

    @rx.event
    def close_settings_dialog(self):
        self.open_settings_dialog_flag = False

    # prompt optimization dialog
    @rx.event
    def open_prompt_optimize_dialog(self):
        self.open_prompt_optimize_dialog_flag = True

    @rx.event
    def close_prompt_optimize_dialog(self):
        self.open_prompt_optimize_dialog_flag = False

    # deploy dialog
    @rx.event
    def open_deploy_dialog(self):
        self.deploy_dialog_flag = True

    @rx.event
    def close_deploy_dialog(self):
        self.deploy_dialog_flag = False
