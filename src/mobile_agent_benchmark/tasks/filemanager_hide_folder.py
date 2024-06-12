from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *


class FileManagerHideFolder(Task):
    def __init__(self, task_name="filemanager_hide_folder",
                 prompt="Hide the folder named 'hidden' and make sure File Manager Stop showing hidden media",
                 min_steps=3,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.hide_folder_name = False

    def setup(self, view_client):
        download_folder = view_client.findViewWithText('Download')
        download_folder.touch()
        view_client.dump()
        create_file_button = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/items_fab')
        create_file_button.touch()
        view_client.dump()
        file_title = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/item_title')
        file_title.setText('hidden')
        view_client.dump()
        Ok_button = view_client.findViewWithText('OK')
        Ok_button.touch()
        view_client.dump()
        moreOptionButton = view_client.findViewWithContentDescription('More options')
        moreOptionButton.touch()

        view_client.dump()
        show_hidden_folder_button = view_client.findViewWithText('Temporarily show hidden')
        if show_hidden_folder_button is not None:
            show_hidden_folder_button.touch()
            view_client.dump()
        return

    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)
    def check_finish(self, view_client, app_event) -> bool:
        folder_name = view_client.findViewWithText('.hidden')
        if folder_name is not None:
            return True
        return False
