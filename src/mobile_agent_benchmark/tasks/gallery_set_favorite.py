from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class GallerySortBySizeAsc(Task):
    def __init__(self, task_name="gallery_set_favorite", 
                 prompt="Go to Downloads Folder and set the first image as favorite", 
                 min_steps=3, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.Click and app_event.id_str == "com.simplemobiletools.gallery.pro:id/bottom_favorite" and "Toggle favorite" in app_event.text_list: 
                return True
        return False
