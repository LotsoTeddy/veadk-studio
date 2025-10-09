import reflex as rx


def agent_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.text("Basic config"),
            rx.form.field(
                rx.form.label("Agent name"),
                rx.input(
                    name="agent_name",
                ),
                class_name="w-4/5",
            ),
            rx.form.field(
                rx.form.label("Agent description"),
                rx.input(
                    name="agent_description",
                ),
                class_name="w-4/5",
            ),
            rx.form.field(
                rx.form.label("Agent instruction"),
                rx.text_area(
                    name="agent_instruction",
                ),
                class_name="w-4/5",
            ),
        ),
        on_submit=[],
    )


def memory_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.text("Memory config"),
            rx.form.field(
                rx.form.label("Long-term memory backend"),
                rx.input(
                    name="long_term_memory_backend",
                ),
                class_name="w-4/5",
            ),
            rx.form.field(
                rx.form.label("Short-term memory backend"),
                rx.input(
                    name="agent_description",
                ),
                class_name="w-full",
            ),
            rx.form.field(
                rx.form.label("Agent instruction"),
                rx.input(
                    name="agent_instruction",
                ),
                class_name="w-full",
            ),
        ),
        on_submit=[],
    )


def knowledgebase_form() -> rx.Component:
    return rx.form(
        rx.vstack(
            rx.text("Knowledgebase config"),
            rx.form.field(
                rx.form.label("Knowledgebase backend"),
                rx.input(
                    name="long_term_memory_backend",
                ),
                class_name="w-full",
            ),
        ),
        on_submit=[],
    )


def build_page() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.heading("Build an agent"),
            rx.text("Powered by VeADK Agent builder", class_name="text-muted"),
            rx.scroll_area(
                agent_form(),
                memory_form(),
                knowledgebase_form(),
                scrollbars="vertical",
                class_name="w-full",
            ),
            height="90vh",
            class_name="min-h-0 w-3/5",
        ),
        spacing="0",
        height="100vh",
        justify="center",
        align="center",
        width="100vw",
        class_name="min-h-0",
    )
