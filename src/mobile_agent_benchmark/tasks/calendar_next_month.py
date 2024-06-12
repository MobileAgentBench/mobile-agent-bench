from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class CalendarNextMonth(Task):
    def __init__(self, task_name="calendar_next_month", 
                 prompt="show events of next month", 
                 min_steps=1, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=2,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.Click and app_event.id_str == "com.simplemobiletools.calendar.pro:id/top_right_arrow":
                return True
        return False
