from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class GallerySortBySizeAsc(Task):
    def __init__(self, task_name="gallery_sort_by_size_asc", 
                 prompt="sort the gallery by size ascendingly", 
                 min_steps=4, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.size_clicked = False
        self.acending_clicked = False
        self.last_event = None

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.Click and app_event.id_str == "com.simplemobiletools.gallery.pro:id/sorting_dialog_radio_size":
                self.size_clicked = True
            if app_event.type == AppEventType.Click and app_event.id_str == "com.simplemobiletools.gallery.pro:id/sorting_dialog_radio_ascending":
                self.acending_clicked = True
            if app_event.type == AppEventType.Click and "OK" in app_event.text_list and self.size_clicked and self.acending_clicked:
                return True
        return False
