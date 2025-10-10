import reflex as rx
from studio.state import ChatState


def event_drawer() -> rx.Component:
    return rx.drawer.portal(
        rx.drawer.content(
            rx.text("Event details", class_name="text-lg font-medium"),
            rx.scroll_area(
                rx.markdown(
                    f"```json\n{ChatState.selected_event_content}\n```",
                )
            ),
            height="100%",
            width="35rem",
            class_name="flex flex-col h-full min-h-0 px-2 py-2",
            background_color="#181818",
            spacing="2",
        )
    )
