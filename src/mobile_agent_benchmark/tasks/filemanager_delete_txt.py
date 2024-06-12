from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .task_utils import *


class FileManagerDeleteTxt(Task):
    def __init__(self, task_name="filemanager_delete_txt",
                 prompt="Delete the txt file in Download folder",
                 min_steps=3,
                 package="com.simplemobiletools.filemanager.pro",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.list = False

    def setup(self, view_client):
        filemanager_permissions(view_client)
        filemanager_create_file_under_download(view_client, "voice.m4a")
        filemanager_create_file_under_download(view_client, "random.txt")
        filemanager_create_file_under_download(view_client, "video.mov")
        

    def teardown(self, view_client):
        filemanager_delete_all_files_under_folder(view_client)

    def check_finish(self, view_client, app_event) -> bool:
        folder = view_client.findViewWithText('> Download')
        voice = view_client.findViewWithText('voice.m4a')
        video = view_client.findViewWithText('video.mov')
        txt = view_client.findViewWithText('random.txt')

        if folder is not None and voice is not None and video is not None and txt is None:
            return True
        return False