from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .contacts_favorite import ContactsFavorite

class ContactsFilter(Task):
    def __init__(self, task_name="contacts_filter",
                 prompt="Change phone filter, which means don't show phone storage in contacts view",
                 min_steps=3,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.prepare = ContactsFavorite()

        self.clicked_phone_storage = False

    # create contact
    def setup(self, view_client):
       self.prepare.setup(view_client)

    # delete contact
    def teardown(self, view_client):
        self.prepare.teardown(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.Click:
                if len(app_event.text_list):
                    if "Phone storage" in app_event.text_list[0]:
                        self.clicked_phone_storage = True
                        print("phone storage clicked")
        if view_client.findViewWithText("Change filter") is not None:
            # if we filtered phone storage, we shouldn't see any contacts
            # and the change filter button will show up
            return self.clicked_phone_storage
        return False