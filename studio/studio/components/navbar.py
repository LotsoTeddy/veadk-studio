from typing import Any

import reflex as rx
from studio.state import ChatState, PageState


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="3", weight="medium", class_name="cursor-pointer"),
        color=rx.color_mode_cond(light=rx.color("black"), dark=rx.color("white")),
        href=url,
    )


def navbar_icon_button(type: str, on_click: Any = []) -> rx.Component:
    return rx.button(
        rx.icon(type), variant="ghost", on_click=on_click, class_name="cursor-pointer"
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/volcengine-color.svg",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("VeADK Studio", size="4", weight="bold"),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_link("Home", "/"),
                    navbar_link(
                        "Documentation", "https://volcengine.github.io/veadk-python/"
                    ),
                    navbar_link("Github", "https://github.com/volcengine/veadk-python"),
                    navbar_icon_button(
                        "settings", on_click=[PageState.open_settings_dialog]
                    ),
                    navbar_icon_button(
                        "plus",
                        on_click=[
                            lambda: ChatState.add_session,
                            # lambda: ChatState.load_session(ChatState.session_id),
                        ],
                    ),
                    navbar_icon_button(
                        "cloud-upload",
                        on_click=[PageState.open_deploy_dialog],
                    ),
                    rx.color_mode.button(),
                    align_items="center",
                    spacing="5",
                ),
                justify="between",
                align_items="center",
                width="100%",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo.jpg",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                    ),
                    rx.heading("Reflex", size="6", weight="bold"),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item("Home"),
                        rx.menu.item("About"),
                        rx.menu.item("Pricing"),
                        rx.menu.item("Contact"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        # bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )
