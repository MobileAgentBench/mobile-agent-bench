from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *


class FileManagerDeleteFile(Task):
    def __init__(self, task_name="filemanager_delete_file",
                 prompt="Delete file named 'testfile.txt' in the 'Downloads' folder",
                 min_steps=3,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.list = False

    def setup(self, view_client):
        filemanager_permissions(view_client)
        filemanager_create_file_under_download(view_client)

    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        file_title_upper = view_client.findViewWithText('Testfile.txt')
        file_title_lower = view_client.findViewWithText('testfile.txt')
        correct_folder_opened = False
        folder = view_client.findViewWithText('> Download')
        # make sure in the same page
        if folder is not None and file_title_upper is None and file_title_lower is None:
            return True
        return False