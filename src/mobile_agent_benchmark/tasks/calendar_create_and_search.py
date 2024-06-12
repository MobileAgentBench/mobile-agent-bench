from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

from .calendar_laundry import CalendarLaundryTask
from .calendar_search import CalendarSearch

class CalendarCreateAndSearch(Task):
    def __init__(self, task_name="calendar_create_and_search", 
                 prompt="Create a new event 'laundry' and then search for it", 
                 min_steps=6, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=12,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.create_task = CalendarLaundryTask()
        self.search_task = CalendarSearch()

        self.create_task_finished = False

    def setup(self, view_client):
        self.create_task.setup(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if not self.create_task_finished:
            self.create_task_finished = self.create_task.check_finish(view_client, app_event)
        else:
            print("create finished, checking search")
            return self.search_task.check_finish(view_client, app_event)
        
        return False