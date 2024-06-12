from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .launcher_rename_app import LauncherRenameApp
from . import task_utils


class LauncherRemoveApp(Task):
    def __init__(
        self,
        task_name="launcher_remove_app",
        prompt="Remove Chrome from Launcher",
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

        self.create_task = LauncherRenameApp()

    # Add Apps
    def setup(self, view_client):
        self.create_task.setup(view_client)

        pass

    def check_finish(self, view_client, app_event) -> bool:
        if (
            view_client.findViewById(
                "com.simplemobiletools.applauncher:id/coordinator_layout"
            )
            is not None
            and view_client.findViewWithText("Camera") is not None
            and view_client.findViewWithText("Chrome") is None
        ):
            return True

        return False
