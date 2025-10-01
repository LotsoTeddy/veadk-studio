import reflex as rx
from studio.consts import GITHUB_CLIENT_ID


def login_page():
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri=http://localhost:3000/auth/callbacks/github"
        f"&scope=read:user"
    )
    return rx.flex(
        rx.link("使用 GitHub 登录", href=github_auth_url, class_name="text-white"),
        rx.link("无状态登陆", href="/main"),
        class_name="flex mx-auto mt-20",
        align="center",
        direction="column",
    )
