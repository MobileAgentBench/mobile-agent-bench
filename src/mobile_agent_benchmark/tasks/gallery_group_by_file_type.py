from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class GalleryGroupByFileType(Task):
    def __init__(self, task_name="gallery_group_by_file_type", 
                 prompt="Go to the downloads folder, group the images by file type", 
                 min_steps=5, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.group_by_file_type_checked = False

    def check_finish(self, view_client: ViewClient, app_event: AppEvent) -> bool:
        if task_utils.is_box_checked(view_client, "com.simplemobiletools.gallery.pro:id/grouping_dialog_radio_file_type"):
            self.group_by_file_type_checked = True
        if app_event is not None:
            if app_event.type == AppEventType.Click and "OK" in app_event.text_list and self.group_by_file_type_checked:
                return True
        return False
