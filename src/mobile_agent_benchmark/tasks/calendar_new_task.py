from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

from .calendar_laundry import CalendarLaundryTask

class CalendarNewTask(Task):
    def __init__(self, task_name="calendar_new_task", 
                 prompt="Create a new task, named 'laundry', with the description of 'wash all my clothes'. Mark it as all-day.", 
                 min_steps=6,
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=14,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.text_filled = False
        self.last_event = None

    def setup(self, view_client) -> bool:
        CalendarLaundryTask().setup(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        title_view = view_client.findViewById('com.simplemobiletools.calendar.pro:id/task_title')
        description_view = view_client.findViewById('com.simplemobiletools.calendar.pro:id/task_description')
        checkbox = view_client.findViewById('com.simplemobiletools.calendar.pro:id/task_all_day')
        if title_view is not None and description_view is not None:
            title = title_view.text()
            description = description_view.text()
            checked = checkbox.checked()
            if title.lower() == 'laundry' and description.lower() == 'wash all my clothes' and checked:
                self.text_filled = True
                print('detected text fill')
        
        if app_event is not None and app_event.package == 'com.simplemobiletools.calendar.pro':
            print('app event received')
            if app_event.type == AppEventType.WindowStateChange:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'Calendar':
                    if self.last_event is not None and self.last_event.type == AppEventType.Click and len(self.last_event.text_list) == 0:
                        # it's a bit weird, but when the text is filled, sometimes the id_str in the save button is missing
                        # it should be `com.simplemobiletools.calendar.pro:id/save`
                        # we use two consecutive events to track the id_button click status:
                        # 1. a click event with no text 
                        # 2. a new page event with text `Calendar`
                        return self.text_filled
            self.last_event = app_event
        return False
