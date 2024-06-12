from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *

class FileManagerCheckStorage(Task):
    def __init__(self, task_name="filemanager_check_storage",
                 prompt="check the storage page",
                 min_steps=1,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=2,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE","android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        filemanager_permissions(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        view_dict = view_client.getViewsById()
        for each_k in view_dict.keys():
            if 'Total storage' in view_dict[each_k].text():
                return True
        return False