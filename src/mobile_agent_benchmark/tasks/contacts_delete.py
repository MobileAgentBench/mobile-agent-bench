from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .contacts_favorite import ContactsFavorite
class ContactsDelete(Task):
    def __init__(self, task_name="contacts_delete",
                 prompt="Delete contact Yuzai",
                 min_steps=3,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.found = False
        self.click = False
        self.prepare = ContactsFavorite()

    def setup(self, view_client):
        self.prepare.setup(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        # Check if the 'Yes' button is clicked
        if app_event is not None and app_event.package == 'com.simplemobiletools.contacts.pro':
            if app_event.type == AppEventType.Click:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'Yes':
                    self.click = True

        # Check if still contains contact 'Yuzai'
        contact_yuzai = view_client.findViewWithText("Yuzai")
        if contact_yuzai is None:
            self.found = True

        return self.click and self.found

