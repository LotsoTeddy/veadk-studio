import reflex as rx
from fastapi import background
from studio.components.chat import chat
from studio.components.choose_agent_dialog import choose_agent_dialog
from studio.components.sidebar import sidebar


def main_page() -> rx.Component:
    return rx.hstack(
        choose_agent_dialog(),
        rx.hstack(
            sidebar(),
            class_name="flex min-h-0",
            width="260px",
            height="100vh",
            background_color="#181818",
            opacity="1",
        ),
        rx.box(
            chat(),
            height="100vh",
            class_name="flex-1 py-2",
            background_color="#212121",
        ),
        spacing="0",
        width="100vw",
        height="100vh",
        class_name="min-h-0",
    )
