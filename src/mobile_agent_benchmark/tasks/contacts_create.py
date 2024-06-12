from ..bench_task import Task
from ..server import AppEvent, AppEventType

class ContactsCreate(Task):
    def __init__(self, task_name="contacts_create",
                 prompt="Create a new contact, his First Name is Yuzai, and his Phone Number is 123456789",
                 min_steps=6,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=12,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.found = False
        self.phone = False
        self.firstname = False

    def teardown(self, view_client):
        print("teardown contact...")
        pkg = "com.simplemobiletools.contacts.pro"
        view_client.device.forceStop(package=pkg)
        view_client.device.startActivity(package=pkg)
        contact = view_client.findViewById('com.simplemobiletools.contacts.pro:id/item_contact_name')
        contact.touch()
        view_client.dump()

        delete_button = view_client.findViewById('com.simplemobiletools.contacts.pro:id/delete')
        delete_button.touch()
        view_client.dump()
        ok_button = view_client.findViewById('android:id/button1')
        ok_button.touch()
        view_client.dump()
        pass

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        first_name = view_client.findViewById('com.simplemobiletools.contacts.pro:id/contact_first_name')
        if first_name is not None:
            text = first_name.text()
            if text.lower() == 'yuzai':
                self.firstname = True

        phone_number = view_client.findViewById('com.simplemobiletools.contacts.pro:id/contact_number')
        if phone_number is not None:
            text = phone_number.text()
            if text == '123456789':
                self.phone = True


        title_views = view_client.findViewById('com.simplemobiletools.contacts.pro:id/item_contact_name')

        if title_views is not None:
            text = title_views.text()
            if text.lower() == 'yuzai':
                print(f"Detected text: {text}")
                self.found = True
        return self.phone and self.firstname and self.found
