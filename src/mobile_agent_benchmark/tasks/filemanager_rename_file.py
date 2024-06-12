from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *

class FileManagerRenameFile(Task):
    def __init__(self, task_name="filemanager_rename_file",
                 prompt="open the folder 'Downloads' and rename the file 'Testfile.txt' to 'testfile1.txt'",
                 min_steps=4,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE","android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.renameFileNameCorrect = False
    def setup(self, view_client):
        filemanager_permissions(view_client)
        filemanager_create_file_under_download(view_client)
    
    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        rename_title = view_client.findViewById('com.simplemobiletools.filemanager.pro:id/rename_item_name')
        if rename_title is not None:
            text = rename_title.text()
            if text.lower() == 'testfile1.txt':
                self.renameFileNameCorrect = True
                print("File name renamed correctly.")
        if app_event is not None and app_event.package == 'com.simplemobiletools.filemanager.pro':
            if app_event.type == AppEventType.WindowStateChange:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'File Manager':
                    if self.last_event is not None and self.last_event.type == AppEventType.Click and self.last_event.text_list[0] == 'OK':
                        return self.renameFileNameCorrect
            self.last_event = app_event
        return False