from typing import Any

import reflex as rx
from studio.state import ChatState, PageState


def navbar_link(text: str, url: str) -> rx.Component:
    return rx.link(
        rx.text(text, size="3", weight="medium", class_name="cursor-pointer"),
        color=rx.color_mode_cond(light=rx.color("black"), dark=rx.color("white")),
        href=url,
    )


# navbar_link("Home", "/"),
#                     navbar_link(
#                         "Documentation", "https://volcengine.github.io/veadk-python/"
#                     ),
#                     navbar_link("Github", "https://github.com/volcengine/veadk-python"),


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
                    on_click=rx.redirect("/main"),
                    class_name="flex cursor-pointer",
                ),
                rx.hstack(
                    rx.button("Documents", on_click=rx.redirect("/"), variant="ghost"),
                    rx.button("Tutorial", on_click=rx.redirect("/"), variant="ghost"),
                    align_items="center",
                    spacing="3",
                    class_name="flex-1",
                ),
                rx.popover.root(
                    rx.popover.trigger(
                        rx.button(
                            rx.avatar(
                                fallback="RX",
                                color_scheme="cyan",
                                class_name="cursor-pointer",
                            ),
                            variant="ghost",
                            class_name="p-0",
                        )
                    ),
                    rx.popover.content(
                        rx.flex(
                            rx.text(ChatState.user_id),
                            direction="column",
                            spacing="3",
                        ),
                    ),
                    class_name="flex ml-auto",
                ),
                spacing="5",
                align_items="center",
                width="100%",
            ),
        ),
        padding="1em",
        width="100%",
    )
