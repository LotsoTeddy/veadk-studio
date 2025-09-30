import reflex as rx


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
            rx.vstack(
                rx.vstack(
                    rx.heading("Input", size="3"),
                    rx.flex(
                        rx.text(
                            "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
                        ),
                        class_name="min-h-0 overflow-y-scroll",
                    ),
                    class_name="min-h-4/9",
                ),
                rx.vstack(
                    rx.heading("Output", size="3"),
                    rx.box(
                        rx.text(
                            "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
                        ),
                        class_name="min-h-0 overflow-y-scroll",
                    ),
                    class_name="min-h-4/9",
                ),
                rx.button("Evaluate", class_name="flex-1 ml-auto"),
                class_name="w-1/2",
            ),
            # right panel
            rx.vstack(
                rx.vstack(
                    rx.heading("Score", size="3"),
                    rx.box(rx.text("0.8")),
                    class_name="min-h-4/9",
                ),
                rx.vstack(
                    rx.heading("Reason", size="3"),
                    rx.box(
                        rx.text(
                            "I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output I am output v I am output I am output I am output I am output v I am output I am output I am output I am output I am output I am output I am output I am outputvI am output I am output I am output I am output "
                        ),
                        class_name="min-h-4/9",
                    ),
                ),
                rx.button("Optimize", class_name="ml-auto flex-1"),
                class_name="w-1/2",
            ),
            spacing="4",
        ),
        # rx.flex(
        #     rx.dialog.close(
        #         rx.button(
        #             "Cancel",
        #             color_scheme="gray",
        #             variant="soft",
        #         ),
        #     ),
        #     rx.dialog.close(
        #         rx.button("Save"),
        #     ),
        #     spacing="3",
        #     margin_top="16px",
        #     justify="end",
        # ),
        class_name="max-w-1/2 max-h-1/2 min-h-0",
    )
