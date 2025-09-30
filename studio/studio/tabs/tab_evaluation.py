import reflex as rx
from studio.components.eval_case_dialog import eval_case_dialog
from studio.state import ChatState


def _evaluation_unit(input: str, output: str) -> rx.Component:
    return rx.card(
        rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label("Input"),
                rx.data_list.value(
                    input,
                    class_name="tracking-tight truncate whitespace-nowrap w-full overflow-hidden",
                ),
                align="start",
            ),
            rx.data_list.item(
                rx.data_list.label("Output"),
                rx.data_list.value(
                    output,
                    class_name="tracking-tight truncate whitespace-nowrap w-full overflow-hidden",
                ),
            ),
            orientation="vertical",
            class_name="flex-1 min-w-0 overflow-x-hidden",
        ),
        # rx.vstack(
        #     rx.text(
        #         rx.text("Input: ", weight="bold"),
        #         input,
        #         size="2",
        #         weight="regular",
        #         class_name="tracking-tight truncate whitespace-nowrap w-full overflow-hidden",
        #         title=input,
        #     ),
        #     rx.text(
        #         rx.text("Output: ", weight="bold"),
        #         output,
        #         size="2",
        #         weight="regular",
        #         class_name="tracking-tight truncate whitespace-nowrap w-full overflow-hidden",
        #         title=output,
        #     ),
        #     spacing="1",
        #     align="start",
        #     class_name="flex-1 min-w-0 overflow-x-hidden",
        # ),
        class_name="w-full flex-1 min-w-0 hover:bg-slate-3 cursor-pointer",
    )


def evaluation_unit(input: str, output: str) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(_evaluation_unit(input, output)),
        eval_case_dialog(),
        class_name="max-h-1/2 max-w-1/2 min-h-0",
    )


def tab_evaluation() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.callout(
                "Evaluation set will be lost after VeADK Studio shutdown.",
                icon="triangle_alert",
                variant="surface",
                color_scheme="yellow",
                class_name="w-full",
            ),
            rx.foreach(
                ChatState.eval_cases,
                lambda eval_case: evaluation_unit(
                    eval_case.input,
                    eval_case.output,
                ),
            ),
            evaluation_unit(
                "你好",
                "我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是我是",
            ),
            spacing="2",
            class_name="w-full min-w-0 box-border",
            width="100%",
        ),
        class_name="flex-1 min-h-0 min-w-0 overflow-y-auto overflow-x-hidden",
    )
