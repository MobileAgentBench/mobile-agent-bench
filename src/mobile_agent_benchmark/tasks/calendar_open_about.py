from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class CalendarOpenAboutTask(Task):
    def __init__(self, task_name="calendar_open_about", 
                 prompt="open about page", 
                 min_steps=2, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

    def check_finish(self, view_client, app_event) -> bool:
        activity_name = view_client.device.getTopActivityName()
        if 'AboutActivity' in activity_name:
            return True
        return False
