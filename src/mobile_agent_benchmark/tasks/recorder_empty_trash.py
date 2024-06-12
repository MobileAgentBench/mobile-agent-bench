from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderEmptyTrash(Task):
    def __init__(self, task_name="recorder_empty_trash", 
                 prompt="go to settings and empty the recycle bin", 
                 min_steps=3, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.RECORD_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        task_utils.recorder_permissions_for_old_android_version(view_client)
        pass

    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.Click and app_event.id_str == 'com.simplemobiletools.voicerecorder:id/settings_empty_recycle_bin_holder':
                return True
        return False