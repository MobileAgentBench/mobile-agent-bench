from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class GalleryRememberPlaybackPosition(Task):
    def __init__(self, task_name="gallery_remember_playback_position", 
                 prompt="Enable remember the last video playback position in settings", 
                 min_steps=4, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def check_finish(self, view_client: ViewClient, app_event: AppEvent) -> bool:
        if task_utils.is_box_checked(view_client, "com.simplemobiletools.gallery.pro:id/settings_remember_last_video_position"):
            return True
        return False
