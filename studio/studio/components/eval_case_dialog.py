import reflex as rx
from studio.state import AgentState, ChatState, PageState


def eval_case_dialog() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Evaluate your case"),
        rx.dialog.description(
            "with LLM-as-a-judge",
            size="2",
            margin_bottom="16px",
        ),
        rx.hstack(
            # left panel
            rx.card(
                rx.text("Test Case", class_name="text-lg font-semibold mb-2"),
                rx.vstack(
                    rx.vstack(
                        rx.heading("Input", size="3"),
                        rx.scroll_area(
                            rx.text(
                                ChatState.selected_eval_case.user_content.parts[0].text
                            ),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[50%] w-full flex flex-col gap-2 min-h-0",
                    ),
                    rx.vstack(
                        rx.heading("Output", size="3"),
                        rx.box(
                            rx.scroll_area(
                                ChatState.selected_eval_case.final_response.parts[
                                    0
                                ].text
                            ),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[50%] w-full flex flex-col gap-2 min-h-0",
                    ),
                    class_name="w-full h-full flex flex-col gap-4 min-h-0 justify-between ",
                ),
                class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
            ),
            # medium panel
            rx.card(
                rx.hstack(
                    rx.text("Judge Model", class_name="text-lg font-semibold"),
                    rx.badge(
                        ChatState.judge_model_name,
                        color_scheme="blue",
                        variant="soft",
                        class_name="text-sm font-semibold rounded-full",
                    ),
                    class_name="items-center mb-2",
                ),
                rx.vstack(
                    rx.vstack(
                        rx.heading("Judge Prompt", size="3"),
                        rx.box(
                            rx.scroll_area(ChatState.judge_model_prompt),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[90%] w-full flex flex-col gap-2 min-h-0",
                    ),
                    rx.flex(
                        rx.button(
                            "Evaluate",
                            class_name="ml-auto",
                            on_click=lambda: ChatState.evaluate_eval_case(
                                AgentState.agent
                            ),
                        ),
                        class_name="h-[10%] w-full items-end justify-end",
                    ),
                    class_name="w-full h-full flex flex-col gap-4 min-h-0 justify-between ",
                ),
                class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
            ),
            # right panel
            rx.card(
                rx.hstack(
                    rx.text("Test Result", class_name="text-lg font-semibold"),
                    rx.badge(
                        ChatState.evaluation_score,
                        color_scheme="green",
                        variant="soft",
                        class_name="text-sm font-semibold rounded-full",
                    ),
                    class_name="items-center mb-2",
                ),
                rx.vstack(
                    rx.vstack(
                        rx.heading("Reason", size="3"),
                        rx.box(
                            rx.scroll_area(ChatState.evaluation_reason),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[90%] w-full flex flex-col gap-2 min-h-0",
                    ),
                    rx.flex(
                        rx.button(
                            "Optimize",
                            class_name="ml-auto",
                            on_click=PageState.open_prompt_optimize_dialog,
                        ),
                        class_name="h-[10%] w-full items-end justify-end",
                    ),
                    class_name="w-full h-full flex flex-col gap-4 min-h-0 justify-between ",
                ),
                class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
            ),
            spacing="4",
            class_name="h-full w-full overflow-hidden",
        ),
        class_name="w-[80vw] max-w-none h-[80vh] max-h-none p-6 flex flex-col overflow-hidden",
    )
