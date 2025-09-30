import reflex as rx


def tab_knowledgebase() -> rx.Component:
    return rx.box(
        rx.text("Knowledgebase tab content goes here."),
        class_name="flex-1 min-h-0 overflow-y-auto",
    )
