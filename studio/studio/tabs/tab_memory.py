import reflex as rx


def tab_memory() -> rx.Component:
    return rx.box(
        rx.text("Memory tab content goes here."),
        class_name="flex-1 min-h-0 overflow-y-auto",
    )
