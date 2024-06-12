from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *

class FileManagerSortFolderBySizeDesc(Task):
    def __init__(self, task_name="filemanager_sort_folder_by_size_desc",
                 prompt="In the main page, sort the folder by size in descending order",
                 min_steps=4,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE","android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.sizeOptionClicked = False
        self.descOptionClicked = False
    def setup(self, view_client):
        filemanager_permissions(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        size_option = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/sorting_dialog_radio_size')
        if size_option is not None:
            text = size_option.text()
            if text.lower() == 'size':
                self.sizeOptionClicked = True
        desc_option = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/sorting_dialog_radio_descending')
        if desc_option is not None:
            text = desc_option.text()
            if text.lower() == 'descending':
               self.descOptionClicked = True
        if app_event is not None and app_event.package == 'com.simplemobiletools.filemanager.pro':
            if app_event.type == AppEventType.WindowStateChange:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'File Manager':
                    if self.last_event is not None and self.last_event.type == AppEventType.Click and self.last_event.text_list[0] == 'OK':
                        return self.sizeOptionClicked and self.descOptionClicked
            self.last_event = app_event
        return False