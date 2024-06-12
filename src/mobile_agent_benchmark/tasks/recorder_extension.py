from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderExtension(Task):
    def __init__(self, task_name="recorder_extension", 
                 prompt="use mp3 as the format for new recordings", 
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
        extension = view_client.findViewWithText("Extension")
        mp3 = view_client.findViewWithText("mp3")
        if extension is not None and mp3 is not None:
            return True
        return False