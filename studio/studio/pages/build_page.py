import reflex as rx


def build_page() -> rx.Component:
    return rx.container(
        rx.card("hello", class_name="mx-auto my-auto min-h-0 max-h-4/5 w-full"),
        spacing="0",
        height="100vh",
        width="100%",
        class_name="min-h-0 min-w-0",
    )
