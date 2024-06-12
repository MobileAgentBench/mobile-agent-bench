from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient
import subprocess
import importlib.resources as pkg_resources


class GallerySetWallpaper(Task):
    def __init__(self, task_name="gallery_set_wallpaper", 
                 prompt="Go to Downloads Folder and set the first image as Home screen wallpaper", 
                 min_steps=6, 
                 package="com.simplemobiletools.gallery.pro", 
                 max_steps=12,
                 stop_after_finish=True,
                 permissions=["android.permission.READ_EXTERNAL_STORAGE", "android.permission.READ_MEDIA_IMAGES", "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_VISUAL_USER_SELECTED", "android.permission.ACCESS_MEDIA_LOCATION"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)
        self.wallpaper_set = False

    def setup(self, view_client):
        #Run adb script to diable system default photos app
        command = ["adb", "shell", "pm", "disable-user", "--user", "0", "com.google.android.apps.photos"]

        subprocess.run(["adb", "push", pkg_resources.files("mobile_agent_benchmark") / "assets/wallpaper.png", "/sdcard/Download/wallpaper.png"])
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("Disabled Google Photos:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Command failed with return code:", e.returncode)
            print("Error output:", e.stderr)
        except Exception as e:
            print("An error occurred:", str(e))
        
        # refresh
        start_x = 540
        start_y = 500
        end_x = 540
        end_y = 1500
        view_client.swipe(start_x, start_y, end_x, end_y)

    def teardown(self, view_client):
        subprocess.run(["adb", "shell", "rm", "-rf", "/sdcard/Download/wallpaper.png"])

    
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.WindowStateChange and "Home screen" in app_event.text_list: 
                self.wallpaper_set = True
            # When Home screen is clicked, there's no click event returned, so we need to check if the window state change event has back to the Simple Wallpaper
            elif app_event.type == AppEventType.WindowStateChange and "Simple Wallpaper" in app_event.text_list and self.wallpaper_set is True:
                return True
        return False
