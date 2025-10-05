import reflex as rx
from studio.consts import GITHUB_CLIENT_ID


def login_page() -> rx.Component:
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri=http://localhost:3000/auth/callbacks/github"
        f"&scope=read:user"
    )

    # return rx.flex(
    #     rx.link("使用 GitHub 登录", href=github_auth_url, class_name="text-white"),
    #     rx.link("无状态登陆", href="/main"),
    #     class_name="flex mx-auto mt-20",
    #     align="center",
    #     direction="column",
    # )

    return rx.card(
        rx.vstack(
            rx.flex(
                rx.image(
                    src="/logo.jpg",
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
                    placeholder="user01",
                    size="3",
                    width="100%",
                ),
                justify="start",
                spacing="2",
                width="100%",
            ),
            rx.button("Start", size="3", width="100%"),
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
            ),
            spacing="6",
            width="100%",
        ),
        size="4",
        max_width="28em",
        width="100%",
        class_name="mx-auto my-auto",
    )
