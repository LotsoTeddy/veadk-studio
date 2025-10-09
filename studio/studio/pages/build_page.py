import reflex as rx


def build_page() -> rx.Component:
    return rx.flex(
        rx.card("hello", class_name="min-h-0 max-h-4/5 w-3/5"),
        spacing="0",
        height="100vh",
        justify="center",
        align="center",
        width="100vw",
        class_name="min-h-0",
    )
