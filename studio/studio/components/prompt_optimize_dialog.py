import reflex as rx
from studio.state import AgentState, PageState


def prompt_optimize_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Optimize your prompt"),
            rx.dialog.description("with Volcengine PromptPilot"),
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
        open=PageState.open_prompt_optimize_dialog_flag,
    )
