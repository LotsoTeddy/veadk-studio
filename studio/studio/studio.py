import reflex as rx

from studio.pages.agent_page import agent_page
from studio.pages.build_page import build_page
from studio.pages.login_page import login_page
from studio.pages.welcome_page import welcome_page
from studio.state import AuthState, ChatState

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Inter:wght@400;500;600;700&family=Roboto:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap",
    ],
    style={"font_family": "var(--font-family)"},
    theme=rx.theme(appearance="dark"),
)

app.add_page(
    login_page,
    title="Login - VeADK Studio - Volcengine Agent Development Kit",
    route="/",
)

app.add_page(
    welcome_page,
    title="VeADK Studio - Volcengine Agent Development Kit",
    route="/main",
)

app.add_page(build_page, route="/build")

app.add_page(
    agent_page,
    route="/agent",
    on_load=[
        ChatState.add_session,
    ],
)


@rx.page(route="/auth/callbacks/github")
def auth_callbacks_github():
    return rx.flex(
        rx.text(
            "Fetching your account information...",
            on_mount=[AuthState.on_load],
        ),
        class_name="flex mx-auto mt-20",
        align="center",
        direction="column",
    )
