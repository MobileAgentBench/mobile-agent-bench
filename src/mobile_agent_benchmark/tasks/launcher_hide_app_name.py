from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .launcher_rename_app import LauncherRenameApp
from . import task_utils


class LauncherHideAppName(Task):
    def __init__(
        self,
        task_name="launcher_hide_app_name",
        prompt="Hide app name in Launcher",
        min_steps=1,
        package="com.simplemobiletools.applauncher",
        max_steps=2,
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
        self.create_task = LauncherRenameApp()

    # Add Apps
    def setup(self, view_client):
        self.create_task.setup(view_client)
        pass

    def check_finish(self, view_client, app_event) -> bool:
        if (
            app_event is not None
            and app_event.type == AppEventType.Click
            and app_event.id_str == "com.simplemobiletools.applauncher:id/toggle_app_name"
        ):
            self.hide_clicked = True

        if view_client.findViewWithText("Chrome") is None and self.hide_clicked:
            return True
        return False
