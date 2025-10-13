import reflex as rx


class PageState(rx.State):
    choose_agent_dialog_flag: bool = False
    open_settings_dialog_flag: bool = False
    open_prompt_optimize_dialog_flag: bool = False
    open_agent_dialog_flag: bool = False
    open_eval_dialog_flag: bool = False
    open_event_drawer_flag: bool = False
    deploy_dialog_flag: bool = False

    @rx.event
    def open_choose_agent_dialog(self):
        self.choose_agent_dialog_flag = True

    @rx.event
    def close_choose_agent_dialog(self):
        self.choose_agent_dialog_flag = False

    # settings dialog
    @rx.event
    def open_settings_dialog(self):
        self.open_settings_dialog_flag = True

    @rx.event
    def close_settings_dialog(self):
        self.open_settings_dialog_flag = False

    # prompt optimization dialog
    @rx.event
    def open_prompt_optimize_dialog(self):
        self.open_prompt_optimize_dialog_flag = True

    @rx.event
    def close_prompt_optimize_dialog(self):
        self.open_prompt_optimize_dialog_flag = False

    # deploy dialog
    @rx.event
    def open_deploy_dialog(self):
        self.deploy_dialog_flag = True

    @rx.event
    def close_deploy_dialog(self):
        self.deploy_dialog_flag = False

    @rx.event
    def open_agent_dialog(self):
        self.open_agent_dialog_flag = True

    @rx.event
    def close_agent_dialog(self):
        self.open_agent_dialog_flag = False

    @rx.event
    def open_eval_dialog(self):
        self.open_eval_dialog_flag = True

    @rx.event
    def close_eval_dialog(self):
        self.open_eval_dialog_flag = False

    @rx.event
    def open_event_drawer(self):
        self.open_event_drawer_flag = True

    @rx.event
    def close_event_drawer(self):
        self.open_event_drawer_flag = False
