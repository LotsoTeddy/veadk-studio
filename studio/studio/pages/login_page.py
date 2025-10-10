import reflex as rx
from studio.consts import GITHUB_CLIENT_ID
from studio.state import ChatState


def login_page() -> rx.Component:
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri=http://localhost:3000/auth/callbacks/github"
        f"&scope=read:user"
    )

    return rx.flex(
        rx.card(
            rx.vstack(
                rx.flex(
                    rx.image(
                        src="/volcengine-color.svg",
                        width="2.5em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading(
                        "Welcome VeADK Studio",
                        size="6",
                        as_="h2",
                        text_align="left",
                        width="100%",
                    ),
                    direction="column",
                    justify="start",
                    spacing="4",
                    width="100%",
                ),
                rx.vstack(
                    rx.text(
                        "User ID",
                        size="3",
                        weight="medium",
                        text_align="left",
                        width="100%",
                    ),
                    rx.input(
                        rx.input.slot(rx.icon("user")),
                        value=ChatState.user_id,
                        on_change=ChatState.set_user_id,  # type: ignore
                        size="3",
                        width="100%",
                    ),
                    justify="start",
                    spacing="2",
                    width="100%",
                ),
                rx.button(
                    "Start",
                    size="3",
                    width="100%",
                    on_click=rx.redirect("/main"),
                    class_name="cursor-pointer",
                ),
                rx.hstack(
                    rx.divider(margin="0"),
                    rx.text(
                        "Or continue with",
                        white_space="nowrap",
                        weight="medium",
                    ),
                    rx.divider(margin="0"),
                    align="center",
                    width="100%",
                ),
                rx.button(
                    rx.icon(tag="github"),
                    "Sign in with Github",
                    variant="outline",
                    size="3",
                    width="100%",
                    on_click=rx.redirect(github_auth_url),
                    class_name="cursor-pointer",
                ),
                spacing="6",
                width="100%",
            ),
            size="4",
            max_width="28em",
            width="100%",
            class_name="mx-auto my-auto",
        ),
        justify="center",
        align="center",
        height="100vh",
        width="100vw",
        style={
            "position": "relative",
            "overflow": "hidden",
            "background": (
                "radial-gradient(circle at 10% 10%, rgba(56, 189, 248, 0.18), transparent 50%), "
                "radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.12), transparent 60%), "
                "rgb(8,10,20)"
            ),
        },
    )
