from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *


class FileManagerSearchFile(Task):
    def __init__(self, task_name="filemanager_search_file",
                 prompt="Search a file named 'testfile.txt'",
                 min_steps=2,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.file_icon_clicked = False

    def setup(self, view_client):
        filemanager_permissions(view_client)
        filemanager_create_file_under_download(view_client)

    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        search = view_client.findViewById("com.simplemobiletools.filemanager.pro:id/top_toolbar_search")
        if search is not None:
            if search.text().lower() == "testfile.txt":
                return True
        return False