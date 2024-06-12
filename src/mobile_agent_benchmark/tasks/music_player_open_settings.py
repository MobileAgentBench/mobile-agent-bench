from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class MusicPlayerOpenSettingsTask(Task):
    def __init__(self, task_name="music_player_open_settings", 
                 prompt="open setting page", 
                 min_steps=2, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=4,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        pass
    def check_finish(self, view_client, app_event) -> bool:
        activity_name = view_client.device.getTopActivityName()
        if 'SettingsActivity' in activity_name:
            return True
        return False