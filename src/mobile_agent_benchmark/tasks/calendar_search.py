from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class CalendarSearch(Task):
    def __init__(self, task_name="calendar_search", 
                 prompt="search event 'laundry'", 
                 min_steps=2, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

    def check_finish(self, view_client, app_event) -> bool:
        search_bar = view_client.findViewById('com.simplemobiletools.calendar.pro:id/top_toolbar_search')
        if search_bar is not None:
            text = search_bar.text()
            if text.lower() == 'laundry':
                return True
        return False