import reflex as rx
from studio.states.agent_state import AgentState
from studio.states.page_state import PageState


def agent_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Agent overview"),
            rx.scroll_area(
                rx.data_list.root(
                    rx.data_list.item(
                        rx.data_list.label("Name"),
                        rx.data_list.value(AgentState.agent.name),
                        align="start",
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Model"),
                        rx.data_list.value(AgentState.agent.model_name),
                        align="start",
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Description"),
                        rx.data_list.value(AgentState.agent.description),
                    ),
                    rx.data_list.item(
                        rx.data_list.label(
                            "System prompt",
                            rx.badge(
                                "Optimize",
                                class_name="ml-2 cursor-pointer",
                                on_click=[PageState.open_prompt_optimize_dialog],
                            ),
                        ),
                        rx.data_list.value(AgentState.agent.instruction),
                    ),
                    rx.cond(
                        AgentState.agent_info.short_term_memory_backend,
                        rx.data_list.item(
                            rx.data_list.label("Short-term memory backend"),
                            rx.data_list.value(
                                rx.badge(
                                    AgentState.agent_info.short_term_memory_backend
                                ),
                            ),
                        ),
                    ),
                    rx.cond(
                        AgentState.agent_info.long_term_memory_backend,
                        rx.data_list.item(
                            rx.data_list.label("Long-term memory backend"),
                            rx.data_list.value(
                                rx.badge(
                                    AgentState.agent_info.long_term_memory_backend
                                ),
                            ),
                        ),
                    ),
                    rx.cond(
                        AgentState.agent_info.knowledgebase_backend,
                        rx.data_list.item(
                            rx.data_list.label("Knowledgebase backend"),
                            rx.data_list.value(
                                rx.badge(AgentState.agent_info.knowledgebase_backend),
                            ),
                        ),
                    ),
                    rx.cond(
                        AgentState.agent,
                        rx.data_list.item(
                            rx.data_list.label("Tools"),
                            rx.data_list.value(
                                rx.hstack(
                                    rx.foreach(
                                        AgentState.agent_info.tools,
                                        lambda tool: rx.badge(tool),
                                    ),
                                    spacing="2",
                                ),
                            ),
                        ),
                    ),
                    orientation="vertical",
                ),
                class_name="flex-1 min-h-0 overflow-y-auto",
            ),
        ),
        open=PageState.open_agent_dialog_flag,
        on_open_change=PageState.close_agent_dialog,
    )
