from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class CalendarLaundryTask(Task):
    def __init__(self, task_name="calendar_laundry", 
                 prompt="Create a new event 'laundry'", 
                 min_steps=4, 
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=8,
                 stop_after_finish=True,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.text_filled = False
        self.last_event = None

    def setup(self, view_client) -> bool:
        # grant app permission by creating a task
        add_button = view_client.findViewById('com.simplemobiletools.calendar.pro:id/calendar_fab')
        add_button.touch()
        view_client.dump()
        event_button = view_client.findViewWithText('Event')
        event_button.touch()
        view_client.dump()
        title_view = view_client.findViewById('com.simplemobiletools.calendar.pro:id/event_title')
        title_view.type('event1')
        save_button = view_client.findViewById('com.simplemobiletools.calendar.pro:id/save')
        save_button.touch()
        view_client.dump()
        ok_button = view_client.findViewWithText('OK')
        ok_button.touch()
        pass

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        title_view = view_client.findViewById('com.simplemobiletools.calendar.pro:id/event_title')
        if title_view is not None:
            text = title_view.text()
            if text.lower() == 'laundry':
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
