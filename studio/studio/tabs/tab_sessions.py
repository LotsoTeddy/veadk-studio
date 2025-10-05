import reflex as rx
from google.adk.sessions import Session
from studio.state import ChatState


def session_unit(session: Session) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(
                session.id,
                size="2",
                weight="regular",
                class_name="font-mono tracking-tight",
            ),
            rx.text(
                f"{ChatState.session_to_num_events_map[session.id]} events",
                size="1",
                weight="regular",
                color="gray",
                class_name="text-grey-800",
            ),
            rx.text(
                f"Last updated at {ChatState.session_to_timestamp_map[session.id]}",
                size="1",
                weight="regular",
                color="gray",
                class_name="text-grey-800",
            ),
            spacing="1",
            align="start",
        ),
        width="100%",
        class_name=rx.cond(
            ChatState.session_id == session.id,
            "bg-slate-4 hover:bg-slate-3 cursor-pointer transition-colors",
            "hover:bg-slate-3 cursor-pointer transition-colors",
        ),
        id=session.id,
        on_click=lambda: ChatState.load_session(session.id),
    )


def tab_sessions() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.foreach(
                ChatState.reversed_sessions,
                lambda session: session_unit(session),
            ),
            spacing="2",
            width="100%",
        ),
        class_name="flex-1 min-h-0 overflow-y-auto",
    )
