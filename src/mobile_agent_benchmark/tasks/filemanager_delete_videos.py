from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *


class FileManagerDeleteVideos(Task):
    def __init__(self, task_name="filemanager_delete_videos",
                 prompt="Delete all videos in Download folder",
                 min_steps=9,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=18,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.list = False

    def setup(self, view_client):
        filemanager_permissions(view_client)
        filemanager_create_file_under_download(view_client, "iccv.mp3")
        filemanager_create_file_under_download(view_client, "icml.mp4")
        filemanager_create_file_under_download(view_client, "aaai.txt")
        filemanager_create_file_under_download(view_client, "corl.avi")
        filemanager_create_file_under_download(view_client, "neurips.exe")
        filemanager_create_file_under_download(view_client, "cvpr.mov")
        

    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        folder = view_client.findViewWithText('> Download')
        if folder is None:
            return False
        should_exist = ["iccv.mp3", "aaai.txt", "neurips.exe"]
        should_delete = ["icml.mp4", "cvpr.mov", "corl.avi"]

        for file in should_exist:
            if view_client.findViewWithText(file) is None:
                return False
        for file in should_delete:
            if view_client.findViewWithText(file) is not None:
                return False
        
        return True