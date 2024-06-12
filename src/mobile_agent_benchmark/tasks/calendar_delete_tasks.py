from ..bench_task import Task
from ..server import AppEvent, AppEventType
from com.dtmilano.android.viewclient import ViewClient

class CalendarDeleteTasks(Task):
    def __init__(self, task_name="calendar_delete_tasks", 
                 prompt="Show events in simple event list, delete the laundry and meeting events.", 
                 min_steps=6,
                 package="com.simplemobiletools.calendar.pro", 
                 max_steps=14,
                 stop_after_finish=False,
                 permissions=["android.permission.POST_NOTIFICATIONS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.text_filled = False
        self.last_event = None

    def setup(self, view_client) -> bool:
        # grant app permission and prepare 3 events. The task needs to delete two of them
        def create_event(name):
            add_button = view_client.findViewById('com.simplemobiletools.calendar.pro:id/calendar_fab')
            add_button.touch()
            view_client.dump()
            event_button = view_client.findViewWithText('Event')
            event_button.touch()
            view_client.dump()
            title_view = view_client.findViewById('com.simplemobiletools.calendar.pro:id/event_title')
            title_view.type(name)
            save_button = view_client.findViewById('com.simplemobiletools.calendar.pro:id/save')
            save_button.touch()
        create_event("Laundry")
        view_client.dump()
        ok_button = view_client.findViewWithText('OK')
        ok_button.touch()

        view_client.dump()
        create_event("Cooking")

        view_client.dump()
        create_event("Meeting")
        pass

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        cooking = view_client.findViewWithText("Cooking")
        laundry = view_client.findViewWithText("Laundry")
        meeting = view_client.findViewWithText("Meeting")

        if cooking is not None and laundry is None and meeting is None:
            return True
        return False
