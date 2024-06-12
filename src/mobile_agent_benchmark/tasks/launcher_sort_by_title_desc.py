from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .launcher_rename_app import LauncherRenameApp
from . import task_utils


class LauncherSortByTitleDesc(Task):
    def __init__(
        self,
        task_name="launcher_sort_by_title_desc",
        prompt="Sort apps by title descending",
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
        self.boxes_checked = False

    # Add Apps
    def setup(self, view_client):
        self.create_task.setup(view_client)

        pass

    def check_finish(self, view_client, app_event) -> bool:
        if task_utils.is_box_checked(
            view_client=view_client,
            id_str="com.simplemobiletools.applauncher:id/sorting_dialog_radio_title",
        ) and task_utils.is_box_checked(
            view_client=view_client,
            id_str="com.simplemobiletools.applauncher:id/sorting_dialog_radio_descending",
        ):
            self.boxes_checked = True

        if (
            app_event is not None
            and app_event.type == AppEventType.Click
            and "OK" in app_event.text_list
            and self.boxes_checked
        ):
            return True
        return False
