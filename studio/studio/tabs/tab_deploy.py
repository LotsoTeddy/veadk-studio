import reflex as rx


def _switch_session(session_id: str):
    pass


def session_unit(session_id: str, timestamp: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(
                session_id,
                size="2",
                weight="regular",
                class_name="font-mono tracking-tight",
            ),
            rx.text(
                timestamp,
                size="1",
                weight="regular",
                color="gray",
                class_name="text-grey-800",
            ),
            spacing="1",
            align="start",
        ),
        width="100%",
        class_name="hover:bg-slate-3 cursor-pointer",
        id=session_id,
        on_click=_switch_session(session_id=session_id),
    )


def tab_deploy() -> rx.Component:
    return rx.vstack(
        rx.form(
            rx.vstack(
                rx.heading("Deploy your agent to VeFaaS", size="4"),
                rx.divider(),
                rx.form.field(
                    rx.form.label("VeFaaS application name"),
                    rx.input(
                        placeholder="First Name",
                        name="vefaas_app_name",
                    ),
                    class_name="w-full",
                ),
                rx.form.field(
                    rx.form.label("Volcengine APIG service name"),
                    rx.input(
                        placeholder="First Name",
                        name="veapig_instance_name",
                    ),
                    class_name="w-full",
                ),
                rx.button("Deploy", type="submit", class_name="ml-auto"),
            ),
            class_name="w-full mt-2",
            # on_submit=FormState.handle_submit,
            reset_on_submit=True,
        ),
        class_name="w-full",
    )
