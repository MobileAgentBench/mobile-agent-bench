from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *

class FileManagerCheckFileProperties(Task):
    def __init__(self, task_name="filemanager_check_file_properties",
                 prompt="open the folder 'Downloads' and check the properties of the file 'testfile.txt'",
                 min_steps=2,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE","android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        filemanager_permissions(view_client)
        filemanager_create_file_under_download(view_client)
    
    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None and app_event.package == 'com.simplemobiletools.filemanager.pro':
            if app_event.type == AppEventType.WindowStateChange:
                if len(app_event.text_list) == 12 and app_event.text_list[0] == 'Properties' and app_event.text_list[2] == 'Testfile.txt':
                    return True
        return False

