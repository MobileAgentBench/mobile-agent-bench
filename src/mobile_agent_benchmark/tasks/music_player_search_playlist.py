from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils
class MusicPlayerSearchPlaylist(Task):
    def __init__(self, task_name="music_player_search_playlist", 
                 prompt="search playlist 'Test'", 
                 min_steps=2, 
                 package="com.simplemobiletools.musicplayer", 
                 max_steps=4,
                 stop_after_finish=False,
                 permissions = ["android.permission.READ_MEDIA_AUDIO", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def setup(self, view_client):
        task_utils.music_player_permissions_for_old_android_version(view_client)
        task_utils.music_player_restore_playlist_functioning(view_client)
        view_dict = view_client.getViewsById()
        for k in view_dict.keys():
            view = view_dict[k]
            if view.map['resource-id'] == 'com.simplemobiletools.musicplayer:id/tab_item_label':
                if view.text().lower() == 'playlists':
                    view.touch()
                    view_client.dump()
                    break
        allView = view_client.getViewsById()
        for(viewId, view) in allView.items():
            viewContext = view.map
            if viewContext['content-desc'] == 'More options':
                view.touch()
                break
        view_client.dump()
        createPlaylistview = view_client.findViewWithText('Create new playlist')
        createPlaylistview.touch()
        view_client.dump()
        playlistTitleView = view_client.findViewById('com.simplemobiletools.musicplayer:id/new_playlist_title')
        playlistTitleView.setText('Test')
        view_client.dump()
        okButton = view_client.findViewWithText('OK')
        okButton.touch()
        view_client.dump()
        pass
    def check_finish(self, view_client, app_event) -> bool:
        search_bar = view_client.findViewById('com.simplemobiletools.musicplayer:id/top_toolbar_search')
        if search_bar is not None:
            text = search_bar.text()
            if text.lower() == 'test':
                return True
        return False