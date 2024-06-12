from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils
class MusicPlayerConfigEqualizer(Task):
    def __init__(self, task_name="music_player_config_equalizer", 
                 prompt="config equalizer to Heavy Metal", 
                 min_steps=3, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=6,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.equalizer_changed = ""
    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        pass
    def check_finish(self, view_client, app_event) -> bool:
        view = view_client.findViewById('com.simplemobiletools.musicplayer:id/equalizer_preset')
        if view is not None:
            self.equalizer_changed = view.text()
            if self.equalizer_changed == "Heavy Metal":
                return True
        return False