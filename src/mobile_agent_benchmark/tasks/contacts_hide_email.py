from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess

class ContactsHideEmail(Task):
    def __init__(self, task_name="contacts_hide_email",
                 prompt="Set not show contact's Email in the contact profile screen",
                 min_steps=5,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.unchecked_email = False

    def setup(self, view_client):
        button_add = view_client.findViewById('com.simplemobiletools.contacts.pro:id/fragment_fab')
        button_add.touch()

        view_client.dump()

        number = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_number')
        number.setText('123456789')

        email = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_email')
        email.setText('yuzai@gmail.com')

        name = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_first_name')
        name.touch()
        view_client.device.type('Yuzai')

        view_client.dump()

        save = view_client.findViewById('com.simplemobiletools.contacts.pro:id/save')
        save.touch()

        view_client.dump()

        contact_yuzai = view_client.findViewWithText('Yuzai')
        contact_yuzai.touch()

        view_client.dump()

        pass

    def teardown(self, view_client):
        subprocess.run(["adb", "shell", "pm", "clear", "com.android.providers.contacts"])

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        email_check = view_client.findViewById('com.simplemobiletools.contacts.pro:id/manage_visible_fields_emails')
        if email_check is not None:
            self.unchecked_email = not email_check.checked()
        
        if app_event is not None:
            if len(app_event.text_list) > 0:
                if 'OK' == app_event.text_list[0]:
                    return self.unchecked_email
        return False
