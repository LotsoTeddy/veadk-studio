import reflex as rx
from studio.state import AgentState, PageState


def deploy_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Optimize your prompt"),
            rx.dialog.description(
                "with Volcengine PromptPilot",
                size="2",
                margin_bottom="16px",
            ),
            rx.hstack(
                rx.vstack(
                    rx.form(
                        rx.form.field(
                            rx.form.label("System prompt"),
                            rx.text_area(
                                default_value=str(AgentState.agent.instruction),
                                name="instruction",
                            ),
                            class_name="w-full",
                        ),
                        rx.button("Replace", type="submit"),
                    )
                ),
                rx.vstack(
                    rx.form(
                        rx.form.field(
                            rx.form.label("Optimize requirements"),
                            rx.text_area(
                                default_value=str(AgentState.agent.instruction),
                                name="instruction",
                            ),
                            class_name="w-full",
                        ),
                        rx.button("Optimize", type="submit"),
                    )
                ),
                rx.vstack(
                    rx.form(
                        rx.form.field(
                            rx.form.label("Final prompt"),
                            rx.text_area(
                                default_value=str(AgentState.agent.instruction),
                                name="instruction",
                            ),
                            class_name="w-full",
                        ),
                        rx.button("Update", type="submit"),
                    )
                ),
            ),
        ),
        open=PageState.deploy_dialog_flag,
        on_open_change=PageState.set_deploy_dialog_flag,
    )
