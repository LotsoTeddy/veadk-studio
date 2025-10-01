import reflex as rx
from studio.components.chat import action_bar, chat
from studio.components.deploy_dialog import deploy_dialog
from studio.components.hints import hints
from studio.components.navbar import navbar
from studio.components.prompt_optimize_dialog import prompt_optimize_dialog
from studio.components.settings_dialog import settings_dialog
from studio.tabs.tab_evaluation import tab_evaluation
from studio.tabs.tab_event import tab_event
from studio.tabs.tab_knowledgebase import tab_knowledgebase
from studio.tabs.tab_memory import tab_memory
from studio.tabs.tab_metadata import tab_metadata
from studio.tabs.tab_sessions import tab_sessions


def agent_page() -> rx.Component:
    return rx.vstack(
        settings_dialog(),
        deploy_dialog(),
        prompt_optimize_dialog(),
        navbar(),
        rx.stack(
            rx.flex(
                rx.card(
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Metadata", value="metadata"),
                            rx.tabs.trigger("Sessions", value="sessions"),
                            rx.tabs.trigger("Event", value="event"),
                            rx.tabs.trigger("Memory", value="memory"),
                            rx.tabs.trigger("Knowledgebase", value="knowledgebase"),
                            rx.tabs.trigger("Evaluation", value="evaluation"),
                        ),
                        rx.tabs.content(
                            tab_metadata(),
                            value="metadata",
                            class_name="flex-1 min-h-0 flex pt-2",
                        ),
                        rx.tabs.content(
                            tab_sessions(),
                            value="sessions",
                            class_name="flex-1 min-h-0 flex pt-2",
                        ),
                        rx.tabs.content(
                            tab_event(),
                            value="event",
                            class_name="flex-1 min-h-0 flex pt-2",
                        ),
                        rx.tabs.content(
                            tab_memory(),
                            value="memory",
                            class_name="flex-1 min-h-0 flex pt-2",
                        ),
                        rx.tabs.content(
                            tab_knowledgebase(),
                            value="knowledgebase",
                            class_name="flex-1 min-h-0 flex pt-2",
                        ),
                        rx.tabs.content(
                            tab_evaluation(),
                            value="evaluation",
                            class_name="flex-1 min-h-0 min-w-0 flex pt-2",
                        ),
                        default_value="metadata",
                        class_name="flex flex-col h-full min-h-0",
                    ),
                    flex="1",
                    class_name="flex-1 min-h-0 min-w-0 box-border",
                ),
                # settings(),
                spacing="3",
                direction="column",
                width="30%",
                height="100%",
                class_name="min-w-0",
            ),
            rx.flex(
                rx.box(
                    chat(),
                    hints(),
                    class_name="relative flex-1 w-full min-h-0",
                ),
                action_bar(),
                direction="column",
                height="100%",
                width="100%",
                flex="1",
                class_name="px-10 min-h-0",
            ),
            spacing="2",
            flex_direction="row",
            padding="1em",
            height="100%",
            width="100%",
            flex="1",
            class_name="min-h-0 min-w-0 flex flex-1",
        ),
        spacing="0",
        height="100vh",
        width="100%",
        class_name="min-h-0 min-w-0",
    )
