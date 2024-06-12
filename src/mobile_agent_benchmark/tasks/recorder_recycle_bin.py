from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class RecorderRecycleBin(Task):
    def __init__(self, task_name="recorder_recycle_bin", 
                 prompt="go to recycle bin page", 
                 min_steps=1, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=2,
                 stop_after_finish=False,
                 permissions=["android.permission.RECORD_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        task_utils.recorder_permissions_for_old_android_version(view_client)
        pass
    
    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None and app_event.type == AppEventType.Click and 'Recycle Bin' in app_event.text_list:
            return True
        return False
