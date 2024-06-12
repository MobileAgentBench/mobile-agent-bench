from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils
class MusicPlayerAlbumSortByYear(Task):
    def __init__(self, task_name="music_player_album_sort_by_year", 
                 prompt="sort the album by 'year'", 
                 min_steps=4, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=8,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.last_event = None
        self.albumClicked = False
    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        pass
    def check_finish(self, view_client, app_event) -> bool:
        albumView = view_client.findViewById('com.simplemobiletools.musicplayer:id/albums_list')
        if albumView is not None :
            self.albumClicked = True
        if app_event is not None and app_event.package == 'com.simplemobiletools.musicplayer':
            print('app event received')
            if app_event.type == AppEventType.Click:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'OK':
                    if self.last_event is not None and self.last_event.type == AppEventType.Click and self.last_event.text_list[0] == 'Year':
                        return self.albumClicked
            self.last_event = app_event
        return False
   