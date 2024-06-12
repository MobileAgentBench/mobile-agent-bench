from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType
import subprocess
from . import task_utils
class MusicPlayerCreatePlayList(Task):
    def __init__(self, task_name="music_player_create_playlist", 
                 prompt="create a new playlist:test", 
                 min_steps=5, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=10,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]
                ):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.text_filled = False
        self.last_event = None

    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        task_utils.music_player_restore_playlist_functioning(view_client)
        pass
    def check_finish(self, view_client, app_event) -> bool:
        view = view_client.findViewById("com.simplemobiletools.musicplayer:id/new_playlist_title")
        if view is not None:
            view_text = view.getText()
            if view_text.lower() == "test":
                self.text_filled = True
                print('detected text fill')
        if app_event is not None and app_event.package == 'com.simplemobiletools.musicplayer':
            print('app event received')
            if app_event.type == AppEventType.WindowStateChange:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'Music Player':
                    if self.last_event is not None and self.last_event.type == AppEventType.Click and self.last_event.text_list[0] == 'OK':
                        return self.text_filled
            self.last_event = app_event
        return False