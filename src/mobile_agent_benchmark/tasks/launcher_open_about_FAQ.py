from ..bench_task import Task
from ..server import AppEvent, AppEventType
from . import task_utils


class LauncherOpenAboutFAQ(Task):
    def __init__(
        self,
        task_name="launcher_open_about_FAQ",
        prompt="Open About page and go Frequently Asked Questions",
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
        if (
            app_event is not None
            and app_event.type == AppEventType.WindowStateChange
            and "Frequently asked questions" in app_event.text_list
        ):
            return True
        return False
