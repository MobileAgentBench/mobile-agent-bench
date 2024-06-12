from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .contacts_favorite import ContactsFavorite

class ContactsSearch(Task):
    def __init__(self, task_name="contacts_search",
                 prompt="Search contact Yuzai",
                 min_steps=2,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.found = False
        self.prepare = ContactsFavorite()

    # create contact
    def setup(self, view_client):
        self.prepare.setup(view_client)

    # delete contact Yuzai
    def teardown(self, view_client):
        self.prepare.teardown(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        search = view_client.findViewById("com.simplemobiletools.contacts.pro:id/top_toolbar_search")
        if search is not None:
            if search.text().lower() == "yuzai":
                return True
        return False