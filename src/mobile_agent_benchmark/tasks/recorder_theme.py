from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderTheme(Task):
    def __init__(self, task_name="recorder_theme", 
                 prompt="change app theme to dark red", 
                 min_steps=6, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=12,
                 stop_after_finish=False,
                 permissions=["android.permission.RECORD_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.theme_correct = False

    def setup(self, view_client):
        task_utils.recorder_permissions_for_old_android_version(view_client)
        pass
    
    def check_finish(self, view_client, app_event) -> bool:
        theme = view_client.findViewWithText("Theme")
        red = view_client.findViewWithText("Dark red")
        if theme is not None and red is not None:
            self.theme_correct = True
        
        if self.theme_correct:
            print("theme correct, waiting for confirm")
            if app_event is not None:
                if app_event.type == AppEventType.Click and app_event.content_desc == 'Save':
                    return True
        return False