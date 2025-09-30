import reflex as rx

from studio.pages.agent_page import agent_page
from studio.state import AgentState, ChatState, PageState


def select_agents() -> rx.Component:
    return rx.select(
        AgentState.list_agents,
        placeholder="Choose local agent",
        value=AgentState.selected_agent,
        on_change=[AgentState.set_agent, ChatState.set_app_name],
    )


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to ", rx.code("VeADK Studio"), size="9"),
            rx.text(
                "Build, debug, and optimize your agent, all in one",
                size="5",
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
    )


app = rx.App(
    # stylesheets=[
    #     "https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Inter:wght@400;500;600;700&family=Roboto:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap",
    # ],
    style={"font_family": "var(--font-family)"},
)

app.add_page(index)

app.add_page(
    agent_page,
    route="/agent",
    on_load=[
        PageState.open_settings_dialog,
    ],
)
