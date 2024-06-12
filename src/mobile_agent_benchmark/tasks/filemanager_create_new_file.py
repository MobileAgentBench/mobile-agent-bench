from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *

class FileManagerCreateNewFile(Task):
    def __init__(self, task_name="filemanager_create_new_file",
                 prompt="Create a new file named 'testfile.txt' in the 'Downloads' folder",
                 min_steps=5,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE","android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        
        self.file_icon_clicked = False

    def setup(self, view_client):
        filemanager_permissions(view_client)

    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)
    
    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None and app_event.package == 'com.simplemobiletools.filemanager.pro':
            if app_event.type == AppEventType.Click and 'File' in app_event.text_list:
                self.file_icon_clicked = True

        correct_folder_opened = False
        folder = view_client.findViewWithText('> Download')
        if folder is not None:
            correct_folder_opened = True
        
        view_dict = view_client.getViewsById()
        for k in view_dict.keys():
            view = view_dict[k]
            if view.map['resource-id'] == 'com.simplemobiletools.filemanager.pro:id/item_name':
                if view.text().lower() == 'testfile.txt':
                    # in case there are other files
                    return correct_folder_opened and self.file_icon_clicked
            
        return False