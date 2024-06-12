from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType
import subprocess
from .music_player_create_playlist import MusicPlayerCreatePlayList
from . import task_utils
class MusicPlayerCreatePlayListAndSearch(Task):
    def __init__(self, task_name="music_player_create_playlist_and_sort_desc", 
                 prompt="create a new playlist: test, and sort all playlist by descending order", 
                 min_steps=7, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=14,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]
                ):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.createTask = MusicPlayerCreatePlayList()
        self.create_task_finished = False
        self.last_event = None
    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        pass
    def check_finish(self, view_client, app_event) -> bool:
        if not self.create_task_finished:
            self.create_task_finished = self.createTask.check_finish(view_client, app_event)
        else:
            print("create finished, checking sorting")
            if app_event is not None and app_event.package == 'com.simplemobiletools.musicplayer':
                if app_event.type == AppEventType.Click:
                    if len(app_event.text_list) == 1 and app_event.text_list[0] == 'OK':
                        if self.last_event is not None and self.last_event.type == AppEventType.Click and self.last_event.text_list[0] == 'Descending':
                            return True
                self.last_event = app_event
        return False