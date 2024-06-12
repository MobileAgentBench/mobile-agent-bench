from ..bench_task import Task
from ..server import AppEvent, AppEventType
from . import task_utils


class LauncherSettingCloseAppWhenLaunching(Task):
    def __init__(
        self,
        task_name="launcher_setting_close_app_when_launching",
        prompt="Change Setting Close this app at launching a different one to false",
        min_steps=3,
        package="com.simplemobiletools.applauncher",
        max_steps=6,
        stop_after_finish=False,
        permissions=[],
    ):
        super().__init__(
            task_name,
            prompt,
            min_steps,
            package,
            max_steps,
            stop_after_finish,
            permissions,
        )

    def setup(self, view_client):
        pass

    def check_finish(self, view_client, app_event) -> bool:
        if view_client.findViewById(
            "com.simplemobiletools.applauncher:id/settings_close_app"
        ) is not None and not task_utils.is_box_checked(
            view_client=view_client,
            id_str="com.simplemobiletools.applauncher:id/settings_close_app",
        ):
            return True
        return False
