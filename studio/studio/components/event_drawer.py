import reflex as rx
from studio.states.chat_state import MessageState


def event_drawer() -> rx.Component:
    return rx.drawer.portal(
        rx.drawer.content(
            rx.text("Event details", class_name="text-lg font-medium", color="white"),
            rx.scroll_area(
                rx.markdown(
                    f"```json\n{MessageState.event_content}\n```",
                ),
                background="inherit",
            ),
            height="100%",
            width="35rem",
            class_name="flex flex-col h-full min-h-0 px-4 py-4",
            background_color="#181818",
            spacing="2",
        )
    )
