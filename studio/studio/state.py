import asyncio
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable

import reflex as rx
import requests
from deepeval.metrics import GEval, ToolCorrectnessMetric
from deepeval.test_case import LLMTestCaseParams
from google.adk.cli.utils import evals
from google.adk.cli.utils.agent_loader import AgentLoader
from google.adk.evaluation.eval_case import EvalCase as ADKEvalCase
from google.adk.evaluation.eval_case import Invocation, SessionInput
from google.adk.evaluation.eval_set import EvalSet as ADKEvalSet
from google.adk.events import Event
from google.adk.sessions import Session
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.base_toolset import BaseToolset
from google.genai.types import Content, Part
from veadk import Runner
from veadk.agent import Agent
from veadk.evaluation.deepeval_evaluator.deepeval_evaluator import DeepevalEvaluator
from veadk.utils.logger import get_logger
from veadk.utils.misc import formatted_timestamp

from studio.consts import GITHUB_CLIENT_ID
from studio.types import Message

logger = get_logger(__name__)

agent_loader = AgentLoader(agents_dir=str(Path.cwd()))

runner: Runner | None = None


class AgentBuildConfig(rx.State):
    agent_name: str = ""
    agent_description: str = ""
    agent_instruction: str = ""

    long_term_memory_backend: str = ""
    long_term_memory_backends: list[str] = [
        "in_memory",
    ]

    short_term_memory_backend: str = ""
    short_term_memory_backends: list[str] = []

    knowledgebase_backend: str = ""
    knowledgebase_backends: list[str] = []

    tools: list[str] = []

    sub_agents: list[Agent] = []


class AgentState(rx.State):
    agent: Agent
    """Global agent instance"""

    selected_agent: str
    """The current selected agent name"""

    tools: list[str]

    knowledgebase_backend: str

    short_term_memory_backend: str

    long_term_memory_backend: str

    system_prompt: str

    optimize_feedback: str = ""

    optimized_prompt: str = ""

    is_optimizing: bool = False

    @rx.var
    def list_agents(self) -> list[str]:
        """List agent from current work directory"""
        return agent_loader.list_agents()

    @rx.event
    async def set_agent(self, agent_name: str):
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
        runner = Runner(agent=self.agent, app_name=agent_name)

        logger.debug(f"Runner init done: {runner}")

        await self._set_agent_metadata()

    @rx.event
    def update_system_prompt(self, data: dict):
        """Update current system prompt to user's input"""
        logger.debug("Update agent system prompt.")
        self.agent.instruction = data["instruction"]
        self.system_prompt = data["instruction"]

    @rx.event
    def replace_system_prompt(self, data: dict):
        """Replace current system prompt to optimized prompt"""
        optimized_prompt = data["optimized_prompt"]
        self.system_prompt = optimized_prompt
        self.agent.instruction = optimized_prompt
        self.optimized_prompt = ""

    @rx.event
    def set_feedback(self, feedback):
        self.optimize_feedback = feedback

    @rx.event
    def optimize_system_prompt(self, data: dict):
        from veadk.integrations.ve_prompt_pilot.ve_prompt_pilot import VePromptPilot

        prompt_pilot_client = VePromptPilot(
            api_key=os.getenv("PROMPT_PILOT_API_KEY", ""),
            workspace_id=os.getenv("PROMPT_PILOT_WORKSPACE_ID", ""),
        )

        self.is_optimizing = True

        self.optimized_prompt = prompt_pilot_client.optimize(
            agents=[self.agent],  # type: ignore
            feedback=data["feedback"],
        )

        self.optimize_feedback = ""

        self.is_optimizing = False

    async def _set_agent_metadata(self):
        if not self.agent:
            rx.redirect("/")

        self.system_prompt = str(self.agent.instruction)

        if self.agent.knowledgebase and isinstance(
            self.agent.knowledgebase.backend, str
        ):
            self.knowledgebase_backend = self.agent.knowledgebase.backend
        else:
            self.knowledgebase_backend = ""

        if self.agent.short_term_memory:
            self.short_term_memory_backend = self.agent.short_term_memory.backend
        else:
            self.short_term_memory_backend = ""

        if self.agent.long_term_memory and isinstance(
            self.agent.long_term_memory.backend, str
        ):
            self.long_term_memory_backend = self.agent.long_term_memory.backend
        else:
            self.long_term_memory_backend = ""

        if self.agent.tools:
            for tool in self.agent.tools:
                if isinstance(tool, Callable):
                    self.tools.append(tool.__name__)
                elif isinstance(tool, BaseTool):
                    self.tools.append(tool.name)
                elif isinstance(tool, BaseToolset):
                    sub_tools = await tool.get_tools()
                    self.tools.extend([tool.name for tool in sub_tools])
                else:
                    logger.error("Invalid tool type.")
        else:
            self.tools = []


class ChatState(rx.State):
    app_name: str = "veadk_studio"
    """One of Google ADK attributes"""

    user_id: str = "user_" + str(uuid.uuid4()).split("-")[0]
    """One of Google ADK attributes"""

    session_id: str
    """One of Google ADK attributes"""

    session: Session
    """Current activated session."""

    sessions: list[Session] = []
    """Maintain sessions for rendering in the session tab"""

    session_to_num_events_map: dict[str, int] = {}
    """Map from session id to number of events in the session"""

    session_to_timestamp_map: dict[str, str] = {}
    """Map from session id to timestamp of the last update time of the session"""

    selected_event_content: str = "No event selected."
    """The currently selected event content"""

    prompt: str
    """User's latest prompt"""

    processing: bool = False
    """Whether processing user's prompt"""

    message_list: list[Message]
    """History message list in current session"""

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

    evaluation_score: str = ""

    evaluation_reason: str = ""

    @rx.event
    def set_user_message(self):
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
        self.processing = True
        yield

        new_message = Content(parts=[Part(text=self.prompt)], role="user")

        global runner
        runner.app_name = self.app_name  # type: ignore
        runner.user_id = self.user_id  # type: ignore

        logger.debug(
            f"Begin generate, app_name: {self.app_name}, user_id: {self.user_id}, session_id: {self.session_id}"
        )

        try:
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
        except Exception as e:
            message = Message(role="assistant", content=str(e))
            yield

        self.prompt = ""

        self.processing = False

        logger.debug("Generate done.")

        session = await self._get_session()
        self.session_to_num_events_map[session.id] = len(session.events)

        # last_update = datetime.fromtimestamp(session.last_update_time)
        # now = datetime.now()
        # self.session_to_timestamp_map[session.id] = humanize.naturaltime(
        #     now - last_update
        # )

        self.session_to_timestamp_map[session.id] = datetime.fromtimestamp(
            session.last_update_time
        ).strftime("%Y-%m-%d %H:%M:%S")

    # evaluation services
    async def update_eval_case(self):
        session = await self._get_session()
        logger.debug(f"Update eval case with session id {session.id}")

        self.eval_cases = evals.convert_session_to_eval_invocations(session)

        if self.eval_cases:
            print(f"invocation id from eval: {self.eval_cases[-1].invocation_id}")

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

        self.evaluation_score = str(evaluator.result_list[0].average_score)
        self.evaluation_reason = evaluator.result_list[0].total_reason

    # session services
    @rx.event
    async def get_event(self, event_id: str):
        session = await self._get_session()

        for event in session.events:
            if event.id == event_id:
                self.selected_event_content = event.model_dump_json(indent=2)

    @rx.event
    async def update_runner_config(self, data: dict | None = None):
        if data:
            app_name = data["app_name"]
            user_id = data["user_id"]
            session_id = data["session_id"]

            self.app_name = app_name
            self.user_id = user_id
            self.session_id = session_id

            await self.add_session()
        else:
            logger.error("Receive no form data!")

    @rx.event
    async def add_session(self):
        """Add a session to current <app_name, user_id>"""
        if not runner:
            rx.redirect("/")

        session_id = "session_" + str(uuid.uuid4()).split("-")[0]

        if runner and runner.short_term_memory:
            await runner.short_term_memory.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=session_id,
            )
            session = await self._get_session(session_id=session_id)

            if session:
                self.session_id = session_id
                self.session = session
                self.sessions.append(session)

                logger.debug(f"Create session with id {session_id}")

            # refresh history messages
            await self.load_session(session_id)

    @rx.event
    async def load_sessions(self):
        if runner and runner.short_term_memory:
            session_service = runner.short_term_memory.session_service

            list_sessions_response = await session_service.list_sessions(
                app_name=self.app_name, user_id=self.user_id
            )
            self.sessions = list_sessions_response.sessions
        else:
            self.sessions = []

    @rx.event
    async def load_session(self, session_id: str):
        """Load session from a session service, and set the history conversations to chat state."""
        self.session_id = session_id

        session = await self._get_session()
        self.session = session

        logger.info(f"Get session with session_id={session.id}")
        logger.info(f"Session has {len(session.events)} events")

        # Step 1: update message list
        _message_list: list[Message] = []
        for event in session.events:
            message = self._event_to_message(event)
            if message:
                _message_list.append(message)
        self.message_list = _message_list

        self.session_to_num_events_map[session.id] = len(session.events)

        self.session_to_timestamp_map[session.id] = datetime.fromtimestamp(
            session.last_update_time
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Step 2: update eval cases
        await self.update_eval_case()

    @rx.var
    def reversed_sessions(self) -> list[Session]:
        return list(reversed(self.sessions))

    @rx.var
    def num_sessions(self) -> int:
        return len(self.sessions)

    def _event_to_message(self, event: Event) -> Message | None:
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
            print(f"invocation id from message: {event.invocation_id}")
            return Message(
                role="assistant",
                content=final_response,
                event_id=event.id,
                invocation_id=event.invocation_id,
            )

    # control services
    # async def handle_key_down(self, key: str):
    #     if key == "Enter":
    #         async for t in self.answer():
    #             yield t

    async def _get_session(self, session_id="") -> Session:
        if not session_id:
            session_id = self.session_id

        if runner and runner.short_term_memory:
            session_service = runner.short_term_memory.session_service

            session = await session_service.get_session(
                app_name=self.app_name, user_id=self.user_id, session_id=session_id
            )

            if not session:
                raise RuntimeError("Session not found.")
        else:
            raise RuntimeError("Runner not set.")

        return session


class PageState(rx.State):
    choose_agent_dialog_flag: bool = False
    open_settings_dialog_flag: bool = False
    open_prompt_optimize_dialog_flag: bool = False
    open_agent_dialog_flag: bool = False
    open_eval_dialog_flag: bool = False
    open_event_drawer_flag: bool = False
    deploy_dialog_flag: bool = False

    @rx.event
    def open_choose_agent_dialog(self):
        self.choose_agent_dialog_flag = True

    @rx.event
    def close_choose_agent_dialog(self):
        self.choose_agent_dialog_flag = False

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

    @rx.event
    def open_agent_dialog(self):
        self.open_agent_dialog_flag = True

    @rx.event
    def close_agent_dialog(self):
        self.open_agent_dialog_flag = False

    @rx.event
    def open_eval_dialog(self):
        self.open_eval_dialog_flag = True

    @rx.event
    def close_eval_dialog(self):
        self.open_eval_dialog_flag = False

    @rx.event
    def open_event_drawer(self):
        self.open_event_drawer_flag = True

    @rx.event
    def close_event_drawer(self):
        self.open_event_drawer_flag = False


class DeployState(rx.State):
    vefaas_application_name: str
    vefaas_apig_instance_name: str

    @rx.var
    def user_project_path(self) -> str:
        return str(Path.cwd())

    @rx.event
    def deploy(self, deploy_config: dict):
        vefaas_application_name = deploy_config["vefaas_application_name"]
        veapig_instance_name = deploy_config["veapig_instance_name"]
        enable_key_auth = deploy_config["enable_key_auth"]

        pass

    @rx.event
    def upload_to_vefaas(self):
        pass


class AuthState(rx.State):
    user_name: str

    user_avatar_url: str

    @rx.event
    def on_load(self):
        code = self.router_data["query"]["code"]
        if code and not self.user_name:
            # Step 1: code -> token
            token_resp = requests.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                    "code": code,
                },
            )
            token_data = token_resp.json()
            access_token = token_data.get("access_token")

            # Step 2: token -> user information
            user_resp = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_resp.json()

            logger.debug(f"Github user_data response: {user_data}")

            if "login" in user_data:
                self.user_name = user_data.get("login")
                self.user_avatar_url = user_data.get("avatar_url")

                logger.debug(f"GitHub user: {self.user_name}")
            else:
                logger.error("Error get user information.")

            return rx.redirect("/welcome")
