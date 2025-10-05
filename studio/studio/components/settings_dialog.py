import reflex as rx
from studio.state import ChatState, PageState


def settings_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Configurations"),
            rx.dialog.description("Set some configurations for your agent runner."),
            rx.form(
                rx.vstack(
                    rx.form.field(
                        rx.form.label("app_name"),
                        rx.input(
                            default_value=ChatState.app_name,
                            name="app_name",
                        ),
                        class_name="w-full",
                    ),
                    rx.form.field(
                        rx.form.label("user_id"),
                        rx.input(
                            default_value=ChatState.user_id,
                            name="user_id",
                        ),
                        class_name="w-full",
                    ),
                    rx.form.field(
                        rx.form.label("session_id"),
                        rx.input(
                            default_value=ChatState.session_id,
                            name="session_id",
                        ),
                        class_name="w-full",
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Done",
                        type="submit",
                        on_click=[
                            PageState.close_settings_dialog,
                        ],
                        class_name="ml-auto",
                    )
                ),
                on_submit=[
                    ChatState.load_sessions,
                    ChatState.update_runner_config,
                ],
            ),
        ),
        open=PageState.open_settings_dialog_flag,
    )
