from pathlib import Path

import reflex as rx


class DeployState(rx.State):
    vefaas_application_name: str
    vefaas_apig_instance_name: str

    @rx.var
    def user_project_path(self) -> str:
        return str(Path.cwd())

    @rx.event
    def deploy(self, deploy_config: dict):
        # vefaas_application_name = deploy_config["vefaas_application_name"]
        # veapig_instance_name = deploy_config["veapig_instance_name"]
        # enable_key_auth = deploy_config["enable_key_auth"]

        pass

    @rx.event
    def upload_to_vefaas(self):
        pass
