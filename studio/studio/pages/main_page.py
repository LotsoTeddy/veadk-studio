from turtle import width

import reflex as rx
from studio.components.chat_bp import chat
from studio.components.sidebar import sidebar


def main_page() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            sidebar(),
            class_name="flex min-h-0",
            width="260px",
            height="100vh",
            style={"background": "#212121"},
        ),
        rx.box(chat(), height="100vh", class_name="flex-1 py-2"),
        width="100vw",
        height="100vh",
        class_name="min-h-0",
    )
