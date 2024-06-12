from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderRename(Task):
    def __init__(self, task_name="recorder_rename", 
                 prompt="rename the first audio to 'voice.m4a'", 
                 min_steps=6, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=12,
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
        view = view_client.findViewById('com.simplemobiletools.voicerecorder:id/recording_title')
        if view is not None:
            return view.text().lower() == 'voice.m4a'
        return False