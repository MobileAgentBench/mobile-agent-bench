from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderDelete(Task):
    def __init__(self, task_name="recorder_delete", 
                 prompt="delete the last recorded audio", 
                 min_steps=5, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=["android.permission.RECORD_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        # To test deleting, we need to at least have something to delete
        # recorder only displays audio recorded by itself
        # so it's not easy to transfer files
        # we need to use UI automation to record an audio
        task_utils.recorder_permissions_for_old_android_version(view_client)
        toggle_button = view_client.findViewById("com.simplemobiletools.voicerecorder:id/toggle_recording_button")
        if toggle_button is None:
            print("setup failed")
            return
        toggle_button.touch()
        time.sleep(1)
        toggle_button.touch()
        pass

    def teardown(self, view_client):
        task_utils.recorder_delete_all()

    def check_finish(self, view_client, app_event) -> bool:
        view = view_client.findViewById("com.simplemobiletools.voicerecorder:id/recordings_placeholder")
        if view is not None:
            return "No recordings" in view.text()
        return False