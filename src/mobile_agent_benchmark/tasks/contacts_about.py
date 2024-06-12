from ..bench_task import Task
from ..server import AppEvent, AppEventType

class ContactsAbout(Task):
    def __init__(self, task_name="contacts_about",
                 prompt="open About View",
                 min_steps=2,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.found = False

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        title_views = view_client.findViewWithText('Frequently asked questions')
        if title_views is not None:
            return True
        return False