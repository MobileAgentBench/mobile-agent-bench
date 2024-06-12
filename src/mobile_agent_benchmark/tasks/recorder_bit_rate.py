from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderBitRate(Task):
    def __init__(self, task_name="recorder_bit_rate", 
                 prompt="change bitrate to 32 kbps", 
                 min_steps=3, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.RECORD_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)


    def check_finish(self, view_client, app_event) -> bool:
        bitrate = view_client.findViewWithText("Bitrate")
        bps = view_client.findViewWithText("32 kbps")
        if bitrate is not None and bps is not None:
            return True
        return False