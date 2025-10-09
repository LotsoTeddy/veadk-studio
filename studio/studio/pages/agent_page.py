import reflex as rx
from studio.components.chat import chat
from studio.components.deploy_dialog import deploy_dialog
from studio.components.hints import hints
from studio.components.navbar import navbar
from studio.components.prompt_optimize_dialog import prompt_optimize_dialog
from studio.components.settings_dialog import settings_dialog
from studio.state import ChatState
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
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.text("Sessions"),
                                    rx.badge(ChatState.num_sessions),
                                    spacing="1",
                                ),
                                value="sessions",
                            ),
                            rx.tabs.trigger(
                                "Event", value="event", id="tab-event-trigger"
                            ),
                            # rx.tabs.trigger("Memory", value="memory"),
                            # rx.tabs.trigger("Knowledgebase", value="knowledgebase"),
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
                spacing="3",
                direction="column",
                width="30%",
                height="100%",
                class_name="min-w-0",
            ),
            chat(),
            spacing="5",
            flex_direction="row",
            padding="1em",
            height="100%",
            width="100%",
            flex="1",
            class_name="min-h-0 min-w-0 flex flex-1 h-full",
        ),
        spacing="1",
        height="100vh",
        width="100%",
        class_name="min-h-0 min-w-0 h-full",
    )
