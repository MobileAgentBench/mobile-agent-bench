from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
from . import task_utils

class GalleryFilterByImagesAndVideos(Task):
    def __init__(self, task_name="gallery_filter_by_images_and_videos", 
                 prompt="filter media in the gallery and only show images and videos", 
                 min_steps=6, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=12,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.last_view_box_status = False

    def check_finish(self, view_client: ViewClient, app_event: AppEvent) -> bool:
        if app_event is not None:
            # Sometimes the "OK" button click message can be missed, so we also check if the window state changes to "Gallery"
            if (app_event.type == AppEventType.Click and "OK" in app_event.text_list) or (app_event.type == AppEventType.WindowStateChange and "Gallery" in app_event.text_list) and self.last_view_box_status is True:
                return True

        if (
            task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/filter_media_images")
            and task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/filter_media_videos")
            and not task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/filter_media_gifs")
            and not task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/filter_media_raws")
            and not task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/filter_media_svgs")
            and not task_utils.is_box_checked(view_client=view_client, id_str="com.simplemobiletools.gallery.pro:id/filter_media_portraits")
        ):
            self.last_view_box_status = True
            
        return False