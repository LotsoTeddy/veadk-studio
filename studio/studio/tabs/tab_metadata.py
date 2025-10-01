import reflex as rx
from studio.components.prompt_optimize_dialog import prompt_optimize_dialog
from studio.state import AgentState, PageState


def tab_metadata() -> rx.Component:
    agent = AgentState.agent

    return rx.scroll_area(
        rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label("Name"),
                rx.data_list.value(agent.name),
                align="start",
            ),
            rx.data_list.item(
                rx.data_list.label("Description"),
                rx.data_list.value(agent.description),
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
                rx.data_list.value(agent.instruction),
            ),
            # rx.cond(
            #     AgentState.agent,
            #     rx.data_list.item(
            #         rx.data_list.label("Tools"),
            #         rx.data_list.value(
            #             rx.hstack(
            #                 *(rx.badge(tool_name) for tool_name in _get_agent_tools()),
            #                 spacing="2",
            #             ),
            #         ),
            #     ),
            # ),
            # rx.data_list.item(
            #     rx.data_list.label("Short-term memory backend"),
            #     rx.data_list.value(
            #         rx.badge(_get_short_term_memory_backend()),
            #     ),
            # ),
            # rx.cond(
            #     _get_long_term_memory_backend(),
            #     rx.data_list.item(
            #         rx.data_list.label("Long-term memory backend"),
            #         rx.data_list.value(
            #             rx.badge(_get_long_term_memory_backend()),
            #         ),
            #     ),
            # ),
            # rx.cond(
            #     _get_knowledgebase_backend(),
            #     rx.data_list.item(
            #         rx.data_list.label("Knowledgebase backend"),
            #         rx.data_list.value(
            #             rx.badge(_get_knowledgebase_backend()),
            #         ),
            #     ),
            # ),
            orientation="vertical",
        ),
        class_name="flex-1 min-h-0 overflow-y-auto px-2",
    )
