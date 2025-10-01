import reflex as rx
from studio.state import AgentState, PageState


def prompt_optimize_dialog() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Optimize your prompt"),
            rx.dialog.description(
                "with Volcengine PromptPilot",
                size="2",
                margin_bottom="16px",
            ),
            rx.hstack(
                rx.card(
                    rx.form(
                        rx.flex(
                            rx.text(
                                "System prompt", class_name="text-lg font-semibold mb-3"
                            ),
                            rx.text_area(
                                default_value=AgentState.system_prompt,
                                name="instruction",
                                class_name=(
                                    "w-full h-full min-h-0 resize-none overflow-y-auto "
                                    "rounded-lg bg-gray-50 ring-1 ring-gray-200 p-3"
                                ),
                            ),
                            class_name="h-[90%] w-full flex flex-col gap-2 min-h-0",
                        ),
                        rx.flex(
                            rx.button("Replace", type="submit"),
                            class_name="h-[10%] w-full items-end justify-end",
                        ),
                        class_name="h-full flex flex-col min-h-0",
                        on_submit=AgentState.update_system_prompt,
                    ),
                    class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
                ),
                rx.card(
                    rx.form(
                        rx.flex(
                            rx.text(
                                "Optimize requirements",
                                class_name="text-lg font-semibold mb-3",
                            ),
                            rx.text_area(
                                default_value=AgentState.optimize_feedback,
                                name="feedback",
                                class_name=(
                                    "w-full h-full min-h-0 resize-none overflow-y-auto "
                                    "rounded-lg bg-gray-50 ring-1 ring-gray-200 p-3"
                                ),
                            ),
                            class_name="h-[90%] w-full flex flex-col gap-2 min-h-0",
                        ),
                        rx.flex(
                            rx.button("Optimize", type="submit"),
                            class_name="h-[10%] w-full items-end justify-end",
                        ),
                        on_submit=AgentState.optimize_system_prompt,
                        class_name="h-full flex flex-col min-h-0",
                    ),
                    class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
                ),
                rx.card(
                    rx.form(
                        rx.flex(
                            rx.text(
                                "Final prompt", class_name="text-lg font-semibold mb-3"
                            ),
                            rx.text_area(
                                default_value=AgentState.optimized_prompt,
                                name="optimized_prompt",
                                class_name=(
                                    "w-full h-full min-h-0 resize-none overflow-y-auto "
                                    "rounded-lg bg-gray-50 ring-1 ring-gray-200 p-3"
                                ),
                            ),
                            class_name="h-[90%] w-full flex flex-col gap-2 min-h-0",
                        ),
                        rx.flex(
                            rx.button("Update", type="submit"),
                            class_name="h-[10%] w-full items-end justify-end",
                        ),
                        on_submit=AgentState.replace_system_prompt,
                        class_name="h-full flex flex-col min-h-0",
                    ),
                    class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
                ),
                spacing="4",
                class_name="h-full w-full overflow-hidden",
            ),
            class_name="w-[80vw] max-w-none h-[80vh] max-h-none p-6 flex flex-col overflow-hidden",
        ),
        open=PageState.open_prompt_optimize_dialog_flag,
        on_open_change=PageState.close_prompt_optimize_dialog,
    )
