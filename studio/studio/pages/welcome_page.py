import reflex as rx
from studio.state import AgentState, AuthState, ChatState


def select_agents() -> rx.Component:
    return rx.select(
        AgentState.list_agents,
        placeholder="Choose local agent",
        value=AgentState.selected_agent,
        on_change=[AgentState.set_agent, ChatState.set_app_name],  # type: ignore
    )


def welcome_page() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.heading("Welcome to ", rx.code("VeADK Studio"), size="9"),
            rx.text(
                "Build, debug, and optimize your agent, all in one",
                size="5",
            ),
            rx.cond(
                AuthState.user_name,
                rx.text(
                    "Current user: ",
                    rx.code(AuthState.user_name),
                    size="5",
                    on_mount=lambda: ChatState.set_user_id(AuthState.user_name),  # type: ignore
                ),
            ),
            rx.stack(
                rx.link(
                    rx.button("Build from scratch"),
                    href="/build",
                    is_external=False,
                ),
                select_agents(),
                # Remote A2A agent
                # rx.link(
                #     rx.button("Remote A2A agent"),
                #     href="https://reflex.dev/docs/getting-started/introduction/",
                #     is_external=False,
                # ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        height="100vh",
        width="100vw",
        justify="center",
        align="center",
    )
