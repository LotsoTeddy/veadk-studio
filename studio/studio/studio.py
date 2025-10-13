import reflex as rx

from studio.pages.build_page import build_page
from studio.pages.login_page import login_page
from studio.pages.main_page import main_page
from studio.states.auth_state import AuthState
from studio.states.page_state import PageState

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Poppins:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Inter:wght@400;500;600;700&family=Roboto:ital,wght@0,400;0,500;0,700;1,400;1,500;1,700&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap",
    ],
    style={"font_family": "var(--font-family)"},
    theme=rx.theme(colors={"text": "white"}),
)

app.add_page(
    login_page,
    title="Login - VeADK Studio - Volcengine Agent Development Kit",
    route="/",
)

app.add_page(build_page, route="/build")

app.add_page(
    main_page,
    route="/main",
    on_load=[
        PageState.open_choose_agent_dialog,
    ],
)


@rx.page(route="/auth/callbacks/github")
def auth_callbacks_github():
    return rx.flex(
        rx.text(
            "Fetching your account information from Github ...",
            on_mount=AuthState.github_auth,
        ),
        class_name="flex mx-auto mt-20",
        align="center",
        direction="column",
    )


@rx.page(route="/auth/callbacks/ve")
def auth_callbacks_ve():
    return rx.flex(
        rx.text(
            "Fetching your account information from Volcengine ...",
            on_mount=AuthState.ve_auth,
        ),
        class_name="flex mx-auto mt-20",
        align="center",
        direction="column",
    )
