import os
from pathlib import Path
from typing import Callable

import reflex as rx
from google.adk.cli.utils.agent_loader import AgentLoader
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.base_toolset import BaseToolset
from veadk import Runner
from veadk.agent import Agent
from veadk.memory import ShortTermMemory
from veadk.utils.logger import get_logger
from veadk.version import VERSION

from studio.types import AgentInfo

logger = get_logger(__name__)

agent_loader = AgentLoader(agents_dir=str(Path.cwd()))

runner: Runner | None = None


class AgentState(rx.State):
    agent: Agent
    """Global agent instance"""

    short_term_memory: ShortTermMemory

    agent_folder_name: str
    """Current selected agent folder name"""

    agent_info: AgentInfo

    optimize_feedback: str = ""

    optimize_prompt: str = ""

    is_optimizing: bool = False

    @rx.var
    def list_agents(self) -> list[str]:
        return agent_loader.list_agents()

    @rx.event
    async def set_agent(self, agent_folder_name: str):
        self.agent_folder_name = agent_folder_name

        agent = agent_loader.load_agent(agent_folder_name)
        assert isinstance(agent, Agent), (
            f"Only support Agent type, but got {agent.__class__.__name__}"
        )
        self.agent = agent

        global runner
        runner = Runner(agent=self.agent, app_name=agent_folder_name)
        self.short_term_memory = runner.short_term_memory  # type: ignore
        logger.debug(f"Runner init done: {runner}")

        self.agent_info = await self._get_agent_info()

    @rx.event
    def set_system_prompt(self, data: dict):
        logger.debug("Update agent system prompt.")
        self.agent.instruction = data["instruction"]

    @rx.event
    def replace_system_prompt(self, data: dict):
        optimized_prompt = data["optimized_prompt"]

        self.agent.instruction = optimized_prompt

    @rx.event
    def optimize_system_prompt(self, data: dict):
        from veadk.integrations.ve_prompt_pilot.ve_prompt_pilot import VePromptPilot

        prompt_pilot_client = VePromptPilot(
            api_key=os.getenv("PROMPT_PILOT_API_KEY", ""),
            workspace_id=os.getenv("PROMPT_PILOT_WORKSPACE_ID", ""),
        )

        self.is_optimizing = True

        self.optimize_prompt = prompt_pilot_client.optimize(
            agents=[self.agent],  # type: ignore
            feedback=data["feedback"],
        )

        self.is_optimizing = False

    @rx.var
    def veadk_version(self) -> str:
        return VERSION

    async def _get_agent_info(self) -> AgentInfo:
        agent_info = AgentInfo()

        if self.agent.knowledgebase and isinstance(
            self.agent.knowledgebase.backend, str
        ):
            agent_info.knowledgebase_backend = self.agent.knowledgebase.backend

        if self.agent.short_term_memory:
            agent_info.short_term_memory_backend = self.agent.short_term_memory.backend

        if self.agent.long_term_memory and isinstance(
            self.agent.long_term_memory.backend, str
        ):
            agent_info.long_term_memory_backend = self.agent.long_term_memory.backend

        if self.agent.tools:
            for tool in self.agent.tools:
                if isinstance(tool, Callable):
                    agent_info.tools.append(tool.__name__)
                elif isinstance(tool, BaseTool):
                    agent_info.tools.append(tool.name)
                elif isinstance(tool, BaseToolset):
                    sub_tools = await tool.get_tools()
                    agent_info.tools.extend([tool.name for tool in sub_tools])
                else:
                    logger.warning(f"Invalid tool type for tool {tool}. Skip it.")

        return agent_info
