import reflex as rx
from studio.components.eval_case_dialog import eval_case_dialog
from studio.components.event_drawer import event_drawer
from studio.components.hints import hints
from studio.states.agent_state import AgentState
from studio.states.chat_state import EvalState, MessageState, SessionState
from studio.states.page_state import PageState
from studio.types import Message


def render_message(message: Message) -> rx.Component:
    user_message_ui = rx.box(
        rx.box(
            rx.cond(
                message.image,
                rx.image(src=message.image, class_name="rounded-lg py-3"),
                rx.markdown(message.content, class_name="[&>p]:!my-2.5", color="white"),
            ),
            class_name="relative px-3 rounded-2xl max-w-[70%] text-white self-end",
            background_color="#323232d9",
        ),
        class_name="flex flex-row group justify-end",
    )

    assistant_message_ui = rx.box(
        rx.vstack(
            rx.box(
                rx.drawer.root(
                    rx.drawer.trigger(
                        rx.markdown(
                            message.content,
                            class_name="[&>p]:!my-2.5 text-white",
                            on_click=[
                                SessionState.load_event(message.event_id),
                                PageState.open_event_drawer,
                            ],
                            color="white",
                        ),
                    ),
                    event_drawer(),
                    rx.drawer.overlay(z_index="5"),
                    direction="left",
                    on_open_change=PageState.close_event_drawer,
                ),
                class_name="px-3 rounded-xl max-w-[100%] text-white self-start hover:bg-slate-2 cursor-pointer",
                on_click=SessionState.load_event(message.event_id),
                _hover={
                    "background": "#323232d9",
                    "transition": "background 0.25s ease",
                },
            ),
            rx.hstack(
                rx.el.button(
                    rx.icon(tag="copy", size=18),
                    class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                    on_click=[
                        rx.set_clipboard(message.content),
                        rx.toast("Copied!"),
                    ],
                ),
                rx.el.button(
                    rx.icon(tag="thumbs-up", size=18),
                    class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                    on_click=[rx.toast("Thanks for your feedback!")],
                ),
                rx.el.button(
                    rx.icon(tag="thumbs-down", size=18),
                    class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                    on_click=[rx.toast("Thanks for your feedback!")],
                ),
                rx.el.button(
                    rx.icon(tag="eye", size=18),
                    class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                    on_click=[rx.toast("Thanks for your feedback!")],
                ),
                rx.dialog.root(
                    rx.dialog.trigger(
                        rx.el.button(
                            rx.icon(tag="play", size=18),
                            class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                            title="Evaluate",
                        ),
                    ),
                    rx.cond(
                        EvalState.eval_cases_map[message.invocation_id],
                        eval_case_dialog(eval_case_id=message.invocation_id),
                    ),
                    class_name="min-h-0",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.el.button(
                            rx.icon(tag="ellipsis", size=18),
                            class_name="p-1 text-slate-10 hover:text-slate-11 transform transition-colors cursor-pointer",
                        ),
                    ),
                    rx.menu.content(
                        rx.menu.item(
                            "Add to CozeLoop dataset",
                            on_click=[rx.toast("Not implemented")],
                        ),
                        size="1",
                    ),
                ),
                class_name="px-3 gap-2",
            ),
            spacing="1",
        )
    )

    tool_call_message_ui = rx.box(
        rx.box(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.markdown(
                        f"**Call `{message.tool_name}`**",
                        class_name="[&>p]:!my-2.5 text-white",
                        on_click=[
                            SessionState.load_event(message.event_id),
                            PageState.open_event_drawer,
                        ],
                        color="white",
                    ),
                ),
                event_drawer(),
                rx.drawer.overlay(z_index="5"),
                direction="left",
                on_open_change=PageState.close_event_drawer,
            ),
            class_name="relative px-3 rounded-xl max-w-[70%] text-slate-12 self-start hover:bg-slate-2 cursor-pointer",
            on_click=SessionState.load_event(message.event_id),
            _hover={
                "background": "#323232d9",
                "transition": "background 0.25s ease",
            },
        ),
        class_name="flex flex-col gap-8 group",
    )

    tool_response_message_ui = rx.box(
        rx.box(
            rx.drawer.root(
                rx.drawer.trigger(
                    rx.markdown(
                        f"**Call `{message.tool_name}` done**",
                        class_name="[&>p]:!my-2.5 text-white",
                        on_click=[
                            SessionState.load_event(message.event_id),
                            PageState.open_event_drawer,
                        ],
                        color="white",
                    ),
                ),
                event_drawer(),
                rx.drawer.overlay(z_index="5"),
                direction="left",
                on_open_change=PageState.close_event_drawer,
            ),
            class_name="relative px-3 rounded-xl max-w-[70%] text-slate-12 self-start hover:bg-slate-2 cursor-pointer",
            on_click=SessionState.load_event(message.event_id),
            _hover={
                "background": "#323232d9",
                "transition": "background 0.25s ease",
            },
        ),
        class_name="flex flex-col gap-8 group",
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
            rx.text(
                AgentState.agent.name, class_name="text-sm font-semibold", color="white"
            ),
            rx.badge(AgentState.agent.model_name, class_name="text-xs"),
            spacing="2",
            align="center",
        ),
        rx.hstack(
            rx.tooltip(
                rx.button(
                    rx.icon("message-square-plus", size=20, color="white"),
                    on_click=[
                        lambda: SessionState.add_session,
                        rx.toast(f"Switch session to {SessionState.session_id}"),
                    ],
                    class_name="cursor-pointer",
                    variant="ghost",
                    _hover={"background": "none"},
                ),
                content="Create a new session",
            ),
            rx.tooltip(
                rx.button(
                    rx.icon("save", size=20, color="white"),
                    on_click=[
                        rx.toast("Save session to long-term memory"),
                    ],
                    class_name="cursor-pointer",
                    variant="ghost",
                    _hover={"background": "none"},
                ),
                content="Save session",
            ),
            spacing="3",
        ),
        class_name="w-1/2 py-2 mx-auto",
        align="center",
        justify="between",
    )


def messages_area() -> rx.Component:
    return rx.auto_scroll(
        rx.box(
            rx.foreach(
                MessageState.message_list,
                lambda message: render_message(message),
            ),
            rx.cond(
                MessageState.processing,
                rx.box(
                    class_name="ml-3 mt-2 h-4 w-4 animate-spin rounded-full border-b-2 border-current",
                    color="white",
                ),
            ),
            class_name="flex flex-col gap-2 py-2 w-1/2 mx-auto",
        ),
        scrollbars="vertical",
        class_name="w-full flex-1 min-h-0",
    )


# def input_bar() -> rx.Component:
#     return rx.box(
#         rx.box(
#             rx.el.input(
#                 placeholder="Ask anything",
#                 on_change=MessageState.set_prompt,  # type: ignore
#                 id="prompt_input",
#                 class_name="box-border px-4 py-2 pr-14 rounded-full w-full outline-none focus:outline-accent-10 h-[48px] text-slate-12 placeholder:text-slate-9",
#                 background_color="#303030",
#                 color="white",
#                 border_width="1px",
#                 border_color="#ffffff0d",
#             ),
#             rx.el.button(
#                 rx.cond(
#                     MessageState.processing,
#                     rx.icon(
#                         tag="loader-circle",
#                         size=19,
#                         color="white",
#                         class_name="animate-spin",
#                     ),
#                     rx.icon(tag="arrow-up", size=19, color="black"),
#                 ),
#                 on_click=[
#                     rx.set_value("prompt_input", ""),
#                     MessageState.set_user_message,
#                     MessageState.generate,
#                 ],
#                 class_name="top-1/2 right-4 absolute disabled:opacity-50 p-1.5 rounded-full transition-colors -translate-y-1/2 cursor-pointer disabled:cursor-default",
#                 disabled=rx.cond(
#                     MessageState.processing | (MessageState.prompt == ""), True, False
#                 ),
#                 background="white",
#             ),
#             class_name="relative w-full",
#         ),
#         class_name="flex flex-col justify-center items-center gap-6 w-full",
#     )


def image_box(image_base64_str: str) -> rx.Component:
    return rx.box(
        rx.image(src=image_base64_str, class_name="h-20 w-20 cursor-pointer"),
        class_name="rounded-lg overflow-hidden flex-shrink-0",
    )


def input_bar() -> rx.Component:
    return rx.vstack(
        # image area
        rx.cond(
            MessageState.user_message_images_draft,
            rx.hstack(
                rx.foreach(
                    MessageState.user_message_images_draft,
                    lambda image_base64_str: image_box(image_base64_str),
                ),
                spacing="2",
                class_name="min-w-0 overflow-x-auto py-1",
            ),
        ),
        # typical area
        rx.hstack(
            # attachment button
            rx.box(
                rx.upload.root(
                    rx.button(
                        rx.icon(tag="plus", size=20, color="white"),
                        class_name="rounded-xl cursor-pointer hover:bg-slate-700",
                        background="transparent",
                    ),
                    id="user_images_upload",
                    on_drop=MessageState.set_user_message_images_draft(
                        rx.upload_files(upload_id="user_images_upload")  # type: ignore
                    ),
                )
            ),
            # text area
            rx.box(
                rx.el.textarea(
                    placeholder="Ask anything",
                    on_change=MessageState.set_user_message_text_draft,  # type: ignore
                    id="prompt_input",
                    width="100%",
                    color="white",
                    border_width="0px",
                    outline="none",
                    auto_height=True,
                    rows=1,
                    resize="none",
                    class_name=(
                        "w-full text-white placeholder:text-slate-400 placeholder:line-height-6"
                        "focus:ring-0 focus:outline-none focus:border-none "
                        "border-none bg-transparent min-h-0 overflow-y-auto my-auto flex"
                    ),
                    background="inherit",
                    style={
                        "maxHeight": "30vh",
                        # "lineHeight": "1.5",
                    },
                    justify="center",
                    align="center",
                ),
                height="100%",
                class_name="flex flex-1 min-h-0 my-auto",
            ),
            # send button
            rx.box(
                rx.button(
                    rx.cond(
                        MessageState.processing,
                        rx.icon(
                            tag="loader-circle",
                            size=20,
                            color="black",
                            class_name="animate-spin",
                        ),
                        rx.icon(tag="arrow-up", size=20, color="black"),
                    ),
                    on_click=[
                        rx.set_value("prompt_input", ""),
                        MessageState.set_user_message,
                        MessageState.generate,
                    ],
                    class_name="rounded-xl cursor-pointer disabled:opacity-50 disabled:cursor-default",
                    disabled=rx.cond(
                        MessageState.processing
                        | (MessageState.user_message_text_draft == ""),
                        True,
                        False,
                    ),
                    background="white",
                )
            ),
            align="end",
            spacing="2",
            class_name="min-w-0 min-h-0 w-full",
        ),
        background_color="#303030",
        color="white",
        border_width="1px",
        border_color="#ffffff0d",
        class_name="min-w-0 min-h-0 rounded-2xl w-1/2 mx-auto px-4 py-2",
    )


def tips() -> rx.Component:
    return rx.text(
        f"VeADK {AgentState.veadk_version} | Session {SessionState.session_id}",
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
        class_name="flex flex-1 min-h-0 h-full w-full",
    )
