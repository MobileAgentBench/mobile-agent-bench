from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class CalendarSnoozeTime(Task):
    def __init__(self, task_name="calendar_snooze_time", 
                 prompt="change snooze time to 1 minute", 
                 min_steps=4, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

    def check_finish(self, view_client, app_event) -> bool:
        view = view_client.findViewById('com.simplemobiletools.calendar.pro:id/settings_snooze_time')
        if view is not None and view.text() == '1 minute':
            return True
        return False
