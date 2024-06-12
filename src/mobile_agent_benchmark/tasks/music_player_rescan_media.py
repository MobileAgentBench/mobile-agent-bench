from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType
import subprocess
import importlib.resources as pkg_resources
from . import task_utils
class MusicPlayerRescanMedia(Task):
    def __init__(self, task_name="music_player_rescan_media", 
                 prompt="rescan media files", 
                 min_steps=2, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=4,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]
                ):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.trackNum = ""
    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        pass
    def teardown(self, view_client):
        """Restore environment
        """
        subprocess.run(["adb", "shell", "rm", "/sdcard/Music/music1.mp3"])
        subprocess.run(["adb", "shell", "rm", "/sdcard/Music/music2.mp3"])
        return
    def check_finish(self, view_client, app_event) -> bool:
        view = view_client.findViewById("com.simplemobiletools.musicplayer:id/folder_tracks")
        if view is not None:
            if view.getText() == "2 Tracks":
                return True
        if app_event is not None and app_event.type == AppEventType.Click:
            if app_event.package == 'com.simplemobiletools.musicplayer' :
                if app_event.text_list[0] == 'More options':
                    subprocess.run(["adb", "push", pkg_resources.files("mobile_agent_benchmark") / "assets/music1.mp3", "/sdcard/Music/music1.mp3"])
                    subprocess.run(["adb", "push", pkg_resources.files("mobile_agent_benchmark") / "assets/music2.mp3", "/sdcard/Music/music2.mp3"])
        return False
        
