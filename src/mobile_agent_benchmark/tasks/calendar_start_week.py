from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class CalendarStartWeek(Task):
    def __init__(self, task_name="calendar_start_week", 
                 prompt="go to settings and make weeks start on Monday", 
                 min_steps=3, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.text_filled = False
        self.last_event = None


    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        view = view_client.findViewById("com.simplemobiletools.calendar.pro:id/settings_start_week_on")
        if view is not None:
            if view.text() == "Monday":
                return True
        return False
