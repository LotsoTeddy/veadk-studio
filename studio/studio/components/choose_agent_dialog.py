import reflex as rx
from studio.state import AgentState, ChatState, PageState


def select_agents() -> rx.Component:
    return rx.select(
        AgentState.list_agents,
        placeholder="Choose local agent",
        value=AgentState.selected_agent,
        on_change=[
            AgentState.set_agent,
            ChatState.set_app_name,
            PageState.close_choose_agent_dialog,
            ChatState.add_session,
        ],
    )


def choose_agent_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Select an agent"),
            rx.dialog.description(
                "From local agent or remote agent",
                size="2",
                margin_bottom="16px",
            ),
            select_agents(),
        ),
        open=PageState.choose_agent_dialog_flag,
        on_open_change=PageState.set_choose_agent_dialog_flag,
    )
