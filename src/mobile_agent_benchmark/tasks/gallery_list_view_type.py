from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class GalleryListViewType(Task):
    def __init__(self, task_name="gallery_list_view_type", 
                 prompt="Change the view type to list view", 
                 min_steps=4, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.view_type = ""

    def check_finish(self, view_client: ViewClient, app_event: AppEvent) -> bool:
        if task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/change_view_type_dialog_radio_grid"):
            self.view_type = "grid"
        elif task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/change_view_type_dialog_radio_list"):
            self.view_type = "list"

        if app_event is not None:
            # Sometimes the "OK" button click message can be missed, so we also check if the window state changes to "Gallery"
            if (app_event.type == AppEventType.Click and "OK" in app_event.text_list) or (app_event.type == AppEventType.WindowStateChange and "Gallery" in app_event.text_list) and self.view_type  == "list":
                return True

