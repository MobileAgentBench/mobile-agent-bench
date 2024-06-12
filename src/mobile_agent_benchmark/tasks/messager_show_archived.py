from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess

class MessagerShowArchivedTask(Task):
    def __init__(self, task_name="messager_show_archived_messages",
                 prompt="show me the archived conversations",
                 min_steps=2,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        return
    
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        archivedView = view_client.findViewWithText('Archive')
        if archivedView is not None:
            return True
        return False