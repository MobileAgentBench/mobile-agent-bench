from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class GalleryUse24HourTimeFormat(Task):
    def __init__(self, task_name="gallery_use_24_hour_time_format", 
                 prompt="Change the date and time format to 24-hour format in gallery settings", 
                 min_steps=5, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.box_24_hour_checked = False

    def check_finish(self, view_client: ViewClient, app_event: AppEvent) -> bool:
        if task_utils.is_box_checked(view_client, "com.simplemobiletools.gallery.pro:id/change_date_time_dialog_24_hour"):
            self.box_24_hour_checked = True
        if app_event is not None:
            if app_event.type == AppEventType.Click and "OK" in app_event.text_list and self.box_24_hour_checked:
                return True
        return False
