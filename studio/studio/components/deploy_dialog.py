import reflex as rx
from studio.state import AgentState, PageState


def deploy_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Deploy to cloud"),
            rx.dialog.description(
                "with Volcengine Function as a Service (VeFaaS)",
                size="2",
                margin_bottom="16px",
            ),
            rx.form(
                rx.vstack(
                    rx.form.field(
                        rx.form.label("Expected application name"),
                        rx.input(
                            default_value=AgentState.selected_agent,
                            name="vefaas_application_name",
                        ),
                        class_name="w-full",
                    ),
                    rx.form.field(
                        rx.form.label("API Gateway instance name"),
                        rx.input(
                            name="veapig_instance_name",
                        ),
                        class_name="w-full",
                    ),
                    rx.form.field(
                        rx.checkbox(
                            name="checkbox",
                            label="Enable KEY Auth",
                            text="Enable KEY Auth",
                        ),
                    ),
                ),
                rx.dialog.close(
                    rx.button(
                        "Deploy",
                        type="submit",
                        on_click=[
                            PageState.close_settings_dialog,
                        ],
                        class_name="ml-auto",
                    )
                ),
                on_submit=[],
            ),
        ),
        open=PageState.deploy_dialog_flag,
        on_open_change=PageState.set_deploy_dialog_flag,
    )
