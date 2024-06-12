from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess

class MessagerFontChangeTask(Task):
    def __init__(self, task_name="messager_change_font_size",
                 prompt="Change the Font size to 'Large' in the settings interface",
                 min_steps=3,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        return

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        fontSizeView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/settings_font_size')
        if fontSizeView is not None:
            text = fontSizeView.text()
            if text.lower() == 'large':
                return True
        return False