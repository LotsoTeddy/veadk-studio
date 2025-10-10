import reflex as rx
from studio.components.hints import hints

# from frontend.components.badge import made_with_reflex
from studio.state import AgentState, AuthState, ChatState, PageState
from studio.types import Message


def render_message(message: Message) -> rx.Component:
    user_message_ui = rx.box(
        rx.box(
            rx.markdown(
                message.content,
                class_name="[&>p]:!my-2.5",
            ),
            class_name="relative bg-slate-3 px-5 rounded-2xl max-w-[70%] text-slate-12 self-end",
        ),
        rx.cond(
            AuthState.user_avatar_url,
            rx.box(
                rx.image(src=AuthState.user_avatar_url, class_name="h-8 w-8"),
                class_name="flex items-center",
            ),
        ),
        class_name="flex flex-row gap-8 pb-10 group justify-end",
    )

    assistant_message_ui = rx.box(
        rx.box(
            rx.box(
                rx.markdown(
                    message.content,
                    class_name="[&>p]:!my-2.5",
                    on_click=[ChatState.get_event(message.event_id)],
                ),
                rx.hstack(
                    rx.el.button(
                        rx.icon(tag="copy", size=18),
                        class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                        on_click=[
                            rx.set_clipboard(message.content),
                            rx.toast("Copied!"),
                        ],
                        title="Copy",
                    ),
                    class_name="-bottom-9 left-3 absolute opacity-0 group-hover:opacity-100 transition-opacity justify-between",
                ),
                class_name="relative px-5 rounded-xl max-w-[70%] text-slate-12 self-start hover:bg-slate-2 cursor-pointer",
                on_click=ChatState.get_event(message.event_id),
            ),
            class_name="flex flex-row gap-4",
        ),
        class_name="flex flex-col gap-8 pb-10 group",
    )

    tool_call_message_ui = rx.box(
        rx.box(
            rx.box(
                rx.image(
                    # src="https://avatar.iran.liara.run/username?username=nihao",
                    src="/doubao-color.svg",
                    class_name="h-8 w-8"
                    + str(rx.cond(ChatState.processing, " animate-pulse", "")),
                ),
                class_name="flex items-center",
            ),
            rx.box(
                rx.markdown(
                    f"Tool call: `{message.tool_name}`",
                    class_name="[&>p]:!my-2.5",
                ),
                class_name="relative bg-accent-4 px-5 rounded-3xl max-w-[70%] text-slate-12 self-start hover:bg-slate-2 cursor-pointer",
                on_click=ChatState.get_event(message.event_id),
            ),
            class_name="flex flex-row gap-6",
        ),
        class_name="flex flex-col gap-8 pb-10 group",
    )

    tool_response_message_ui = rx.box(
        rx.box(
            rx.box(
                rx.image(
                    # src="https://avatar.iran.liara.run/username?username=nihao",
                    src="/doubao-color.svg",
                    class_name="h-8 w-8"
                    + str(rx.cond(ChatState.processing, " animate-pulse", "")),
                ),
                class_name="flex items-center",
            ),
            rx.box(
                rx.markdown(
                    f"Tool call: `{message.tool_name}` done",
                    class_name="[&>p]:!my-2.5",
                ),
                class_name="relative bg-accent-4 px-5 rounded-3xl max-w-[70%] text-slate-12 self-start hover:bg-slate-2 cursor-pointer",
                on_click=ChatState.get_event(message.event_id),
            ),
            class_name="flex flex-row gap-6",
        ),
        class_name="flex flex-col gap-8 pb-10 group",
    )

    return rx.match(
        message.role,
        ("user", user_message_ui),
        ("assistant", assistant_message_ui),
        ("tool_call", tool_call_message_ui),
        ("tool_response", tool_response_message_ui),
        rx.box("Unknown role"),
    )  # type: ignore


def info_bar() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.image(src="/agent_avatar.webp", class_name="h-8 w-8"),
            rx.text(AgentState.agent.name, class_name="text-sm font-semibold"),
            rx.badge(AgentState.agent.model_name, class_name="text-xs"),
            spacing="2",
            align="center",
        ),
        rx.hstack(
            rx.tooltip(
                rx.button(
                    rx.icon("message-square-plus", size=20, color="white"),
                    on_click=[
                        lambda: ChatState.add_session,
                    ],
                    class_name="cursor-pointer",
                    variant="ghost",
                ),
                content="Create a new session",
            ),
            # rx.button(
            #     rx.icon("settings", size=16),
            #     "Settings",
            #     size="1",
            #     on_click=[PageState.open_settings_dialog],
            #     class_name="cursor-pointer",
            #     variant="ghost",
            # ),
            spacing="3",
        ),
        class_name="w-full py-2",
        align="center",
        justify="between",
    )


def messages_area() -> rx.Component:
    return rx.scroll_area(
        rx.foreach(
            ChatState.message_list,
            lambda message: render_message(message),
        ),
        scrollbars="vertical",
        class_name="flex w-full flex-1 min-h-0",
    )


def input_bar() -> rx.Component:
    return rx.box(
        rx.box(
            rx.el.input(
                placeholder="Ask anything",
                on_change=ChatState.set_prompt,
                id="prompt_input",
                class_name="box-border bg-slate-3 px-4 py-2 pr-14 rounded-full w-full outline-none focus:outline-accent-10 h-[48px] text-slate-12 placeholder:text-slate-9",
            ),
            rx.el.button(
                rx.cond(
                    ChatState.processing,
                    rx.icon(
                        tag="loader-circle",
                        size=19,
                        color="white",
                        class_name="animate-spin",
                    ),
                    rx.icon(tag="arrow-up", size=19, color="white"),
                ),
                on_click=[
                    rx.set_value("prompt_input", ""),
                    ChatState.set_user_message,
                    ChatState.generate,
                ],
                class_name="top-1/2 right-4 absolute bg-accent-9 hover:bg-accent-10 disabled:hover:bg-accent-9 disabled:opacity-50 p-1.5 rounded-full transition-colors -translate-y-1/2 cursor-pointer disabled:cursor-default",
                disabled=rx.cond(
                    ChatState.processing | (ChatState.prompt == ""), True, False
                ),
            ),
            class_name="relative w-full",
        ),
        class_name="flex flex-col justify-center items-center gap-6 w-full",
    )


def tips() -> rx.Component:
    return rx.text(
        f"VeADK version: 0.2.0 | Current session: {ChatState.session_id}",
        class_name="text-xs text-slate-9 mx-auto",
    )


def chat() -> rx.Component:
    return rx.vstack(
        info_bar(),
        rx.box(
            messages_area(),
            hints(),
            class_name="relative flex-1 w-full min-h-0",
        ),
        input_bar(),
        tips(),
        spacing="3",
        width="50rem",
        class_name="flex flex-1 min-h-0 h-full mx-auto",
    )
