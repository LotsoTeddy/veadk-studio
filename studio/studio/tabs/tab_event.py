import reflex as rx
from studio.state import ChatState


def tab_event() -> rx.Component:
    return rx.box(
        rx.markdown(f"```json\n{ChatState.selected_event_content}\n```"),
        class_name="flex-1 min-h-0 overflow-y-auto",
    )
