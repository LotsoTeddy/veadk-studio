import reflex as rx
from studio.state import PageState

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
                rx.text("Test Case", class_name="text-lg font-semibold mb-3"),
                rx.vstack(
                    rx.vstack(
                        rx.heading("Input", size="3"),
                        rx.box(
                            rx.text(
                                "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
                            ),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[50%] w-full flex flex-col gap-2 min-h-0",
                    ),
                    rx.vstack(
                        rx.heading("Output", size="3"),
                        rx.box(
                            rx.text(
                                "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
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
                rx.text(
                    "Judge Model Config",
                    class_name="text-lg font-semibold mb-3"
                ),
                rx.vstack(
                    rx.vstack(
                        rx.heading("Judge Prompt", size="3"),
                        rx.box(
                            rx.text(
                                "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
                            ),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[90%] w-full flex flex-col gap-2 min-h-0",
                    ),
                    rx.flex(
                        rx.button("Evaluate", class_name="ml-auto"),
                        class_name="h-[10%] w-full items-end justify-end",
                    ),
                    class_name="w-full h-full flex flex-col gap-4 min-h-0 justify-between ",
                ),
                class_name="w-1/3 h-full flex flex-col gap-4 min-h-0 shadow-sm p-4",
            ),
        
            # right panel
            rx.card(
                rx.hstack(
                    rx.text(
                        "Test Result",
                        class_name="text-lg font-semibold"
                    ),
                    rx.badge(
                        "0.8",
                        color_scheme="green",
                        variant="soft",
                        class_name="text-sm font-semibold rounded-full"
                    ),
                    class_name="items-center mb-3"
                ),
                rx.vstack(
                    rx.vstack(
                        rx.heading("Reason", size="3"),
                        rx.box(
                            rx.text(
                                "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
                            ),
                            class_name="w-full h-full overflow-y-auto rounded-lg scroll-clean",
                        ),
                        class_name="h-[90%] w-full flex flex-col gap-2 min-h-0 ",
                    ),
                    rx.flex(
                        rx.button(
                            "Optimize", 
                            class_name="ml-auto"),
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
