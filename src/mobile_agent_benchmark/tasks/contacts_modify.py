from ..bench_task import Task
from ..server import AppEvent, AppEventType
from .contacts_favorite import ContactsFavorite
class ContactsModify(Task):
    def __init__(self, task_name="contacts_modify",
                 prompt="Change the contact Yuzai's number to 987654321 and save it",
                 min_steps=4,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.found = False
        self.name = False
        self.number = False
        self.prepare = ContactsFavorite()

    # create contact
    def setup(self, view_client):
        self.prepare.setup(view_client)

    # delete contact
    def teardown(self, view_client):
        self.prepare.teardown(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        try:
            contact_name = view_client.findViewById('com.simplemobiletools.contacts.pro:id/contact_name')
            if contact_name is not None:
                text = contact_name.text()
                if text.lower() == 'yuzai':
                    self.name = True

            phone_number = view_client.findViewById('com.simplemobiletools.contacts.pro:id/contact_number')
            if phone_number is not None:
                text = phone_number.text()
                if text == '987654321':
                    self.number = True
            return self.name and self.number
        except Exception as e:
            print(f"Exception: {str(e)}")
            return False