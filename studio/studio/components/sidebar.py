from typing import Callable

import reflex as rx
from google.adk.sessions import Session
from studio.components.deploy_dialog import deploy_dialog
from studio.components.prompt_optimize_dialog import prompt_optimize_dialog
from studio.state import ChatState, PageState


def logo_area() -> rx.Component:
    return rx.hstack(
        rx.image(src="/volcengine-color.svg", class_name="h-6 w-6"),
        # rx.text("VeADK Studio", class_name="text-sm font-semibold"),
        spacing="2",
        align="center",
        justify="start",
        width="100%",
        class_name="px-2 py-1",
    )


def option_item(icon: str, title: str, on_click: list = []) -> rx.Component:
    return rx.hstack(
        rx.icon(icon, size=18),
        rx.text(title, class_name="text-sm"),
        rx.icon(
            "chevron-right",
            class_name="ml-auto opacity-0 hover:opacity-100 transition-opacity duration-200",
            size=18,
        ),
        align="center",
        class_name="px-2 py-2 hover:bg-slate-3 rounded-lg cursor-pointer w-full",
        on_click=on_click,
    )


def option_area() -> rx.Component:
    return rx.vstack(
        option_item("bot", "Agent"),
        option_item(
            "sparkles", "Prompt", on_click=[PageState.open_prompt_optimize_dialog]
        ),
        option_item("cloud", "Deploy", on_click=[PageState.open_deploy_dialog]),
        spacing="1",
        width="100%",
    )


def session_item(session: Session) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(session.id, class_name="text-sm"),
            rx.text(
                f"{ChatState.session_to_num_events_map[session.id]} events",
                class_name="text-xs text-slate-9",
            ),
            spacing="0",
        ),
        rx.icon("chevron-right", class_name="ml-auto", size=20),
        align="center",
        class_name="px-2 py-2 hover:bg-slate-3 rounded-lg cursor-pointer w-full",
    )


def session_area() -> rx.Component:
    return rx.vstack(
        rx.text(
            "Sessions", class_name="px-2 text-slate-11 uppercase text-xs font-semibold"
        ),
        rx.scroll_area(
            rx.vstack(
                rx.foreach(
                    ChatState.reversed_sessions,
                    lambda session: session_item(session),
                ),
                spacing="1",
                width="100%",
            ),
            scrollbars="vertical",
            class_name="flex-1 min-h-0 w-full",
        ),
        class_name="flex-1 min-h-0",
        width="100%",
    )


def user_area() -> rx.Component:
    return rx.hstack(
        rx.avatar(
            fallback="RX", color_scheme="cyan", class_name="cursor-pointer", size="3"
        ),
        rx.vstack(
            rx.text("User", class_name="text-sm font-semibold"),
            rx.text("View Profile", class_name="text-xs text-slate-9"),
            spacing="1",
        ),
        class_name="px-2 py-2 hover:bg-slate-3 rounded-lg cursor-pointer w-full mt-auto",
    )


def sidebar() -> rx.Component:
    return rx.vstack(
        prompt_optimize_dialog(),
        deploy_dialog(),
        logo_area(),
        option_area(),
        session_area(),
        user_area(),
        spacing="3",
        align="start",
        class_name="min-h-0 h-full w-full px-2 py-2",
        style={"background": "#181818"},
    )
