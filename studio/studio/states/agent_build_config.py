import reflex as rx
from veadk import Agent


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
