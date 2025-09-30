import reflex as rx
from studio.state import ChatState


def session_unit(session_id: str, timestamp: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(
                session_id,
                size="2",
                weight="regular",
                class_name="font-mono tracking-tight",
            ),
            rx.text(
                timestamp,
                size="1",
                weight="regular",
                color="gray",
                class_name="text-grey-800",
            ),
            spacing="1",
            align="start",
        ),
        width="100%",
        class_name="hover:bg-slate-3 cursor-pointer",
        id=session_id,
        on_click=lambda: ChatState.load_session(session_id),
    )


def tab_sessions() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.foreach(
                ChatState.session_ids,
                lambda session_id: session_unit(session_id, "2025-09-28 13:59:09"),
            ),
            spacing="2",
            width="100%",
        ),
        class_name="flex-1 min-h-0 overflow-y-auto",
    )
