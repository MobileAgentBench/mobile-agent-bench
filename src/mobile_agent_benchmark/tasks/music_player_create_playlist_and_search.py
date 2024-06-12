from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType
import subprocess
from .music_player_create_playlist import MusicPlayerCreatePlayList
from .music_player_search_playlist import MusicPlayerSearchPlaylist
from . import task_utils
class MusicPlayerCreatePlayListAndSearch(Task):
    def __init__(self, task_name="music_player_create_playlist_and_search", 
                 prompt="create a new playlist: test, and search for it", 
                 min_steps=7, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=14,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]
                ):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.createTask = MusicPlayerCreatePlayList()
        self.searchTask = MusicPlayerSearchPlaylist()
        self.create_task_finished = False
    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        task_utils.music_player_restore_playlist_functioning(view_client)
        pass
    def check_finish(self, view_client, app_event) -> bool:
        if not self.create_task_finished:
            self.create_task_finished = self.createTask.check_finish(view_client, app_event)
        else:
            print("create finished, checking search")
            return self.searchTask.check_finish(view_client, app_event)
        return False