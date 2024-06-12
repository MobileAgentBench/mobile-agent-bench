from ..bench_task import Task
from ..server import AppEvent, AppEventType
from . import task_utils


class LauncherAddApps(Task):
    def __init__(
        self,
        task_name="launcher_add_apps",
        prompt="Add Chrome and Camera to launcher",
        min_steps=4,
        package="com.simplemobiletools.applauncher",
        max_steps=8,
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
        self.camera_added = False
        self.chrome_added = False
        self.ok_clicked = False

    def check_finish(self, view_client, app_event) -> bool:
        # Check if the favorite button is clicked
        if app_event is not None:
            if app_event.type == AppEventType.Click and "Camera" in app_event.text_list:
                self.camera_added = True
            if app_event.type == AppEventType.Click and "Chrome" in app_event.text_list:
                self.chrome_added = True
            if app_event.type == AppEventType.Click and "OK" in app_event.text_list:
                self.ok_clicked = True
            if self.camera_added and self.chrome_added and self.ok_clicked:
                return True
        return False
