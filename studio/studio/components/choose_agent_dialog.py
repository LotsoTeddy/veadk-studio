import reflex as rx
from studio.states.agent_state import AgentState
from studio.states.chat_state import MessageState
from studio.states.page_state import PageState


def select_agents() -> rx.Component:
    return rx.select(
        AgentState.list_agents,
        placeholder="Choose local agent",
        value=AgentState.agent_folder_name,
        on_change=[
            AgentState.set_agent,  # type: ignore
            MessageState.set_app_name,  # type: ignore
            MessageState.add_session,
            PageState.close_choose_agent_dialog,
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
    )
