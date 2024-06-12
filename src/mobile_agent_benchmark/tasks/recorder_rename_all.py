from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import time
from . import task_utils

class RecorderRenameAll(Task):
    def __init__(self, task_name="recorder_rename_all", 
                 prompt="rename all audio to voice1.m4a, voice2.m4a, and so on", 
                 min_steps=13, 
                 package="com.simplemobiletools.voicerecorder", 
                 max_steps=26,
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
        for i in range(3): # record 3 audio
            toggle_button.touch()
            time.sleep(1)
            toggle_button.touch()


    def teardown(self, view_client):
        task_utils.recorder_delete_all()

    def check_finish(self, view_client, app_event) -> bool:
        view1 = view_client.findViewWithText('voice1.m4a')
        view2 = view_client.findViewWithText('voice2.m4a')
        view3 = view_client.findViewWithText('voice3.m4a')
        if view1 is not None and view2 is not None and view3 is not None:
            return True
        return False