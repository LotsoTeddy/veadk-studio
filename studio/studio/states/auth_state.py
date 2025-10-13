import os
from typing import Literal

import reflex as rx
import requests
from veadk.utils.logger import get_logger

from studio.consts import (
    GITHUB_CLIENT_ID,
    VE_CLIENT_ID,
    VE_CLIENT_SECRET,
    VE_TOKEN_ENDPOINT,
    VE_USERINFO_ENDPOINT,
)
from studio.states.chat_state import MessageState

logger = get_logger(__name__)


class AuthState(rx.State):
    user_name: str

    user_avatar_url: str

    user_type: Literal["Github", "Volcengine"] | None = None

    @rx.event
    def github_auth(self):
        code = self.router_data["query"]["code"]
        if code and not self.user_name:
            # Step 1: code -> token
            token_resp = requests.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
                    "code": code,
                },
            )
            token_data = token_resp.json()
            access_token = token_data.get("access_token")

            # Step 2: token -> user information
            user_resp = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Accept": "application/json",
                },
            )
            user_data = user_resp.json()

            logger.debug(f"Github user_data response: {user_data}")

            if "login" in user_data:
                self.user_name = user_data.get("login")
                self.user_avatar_url = user_data.get("avatar_url")
                self.user_type = "Github"

                logger.debug(f"GitHub user: {self.user_name}")
            else:
                logger.error("Error get user information.")

        return rx.redirect("/main")

    @rx.event
    async def ve_auth(self):
        code = self.router_data["query"]["code"]
        if code and not self.user_name:
            # Step 1: code -> token
            token_resp = requests.post(
                VE_TOKEN_ENDPOINT,
                headers={"Accept": "application/json"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": VE_CLIENT_ID,
                    "client_secret": VE_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": "http://localhost:3000/auth/callbacks/ve",
                },
            )

            access_token = ""
            if token_resp.status_code == 200:
                access_token = token_resp.json().get("access_token")

            # Step 2: token -> user information
            if access_token:
                user_resp = requests.get(
                    VE_USERINFO_ENDPOINT,
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Accept": "application/json",
                    },
                )

                user_data = user_resp.json()
                logger.debug(f"Volcengine user_data response: {user_data}")
                self.user_name = user_data.get("email", "") or user_data.get("sub", "")
                message_state = await self.get_state(MessageState)
                message_state.set_user_id(self.user_name)

                self.user_type = "Volcengine"

                logger.debug(f"Volcengine user: {self.user_name}")

        return rx.redirect("/main")
