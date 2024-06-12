from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess


class ContactsFavorite(Task):
    def __init__(self, task_name="contacts_favorite",
                 prompt="Set the contact Yuzai to Favorite",
                 min_steps=2,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

    # create contact
    def setup(self, view_client):
        # touch '+' button
        button_add = view_client.findViewById('com.simplemobiletools.contacts.pro:id/fragment_fab')
        button_add.touch()

        view_client.dump()

        # input firstname
        try:
            element = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_first_name')
            element.touch()

            view_client.device.type('Yuzai')
        except Exception as e:
            print("ExceptionName: ", str(e))

        # input phone number
        try:
            element = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_number')
            element.setText('123456789')
        except Exception as e:
            print("ExceptionNumber: ", str(e))

        # click save button
        try:
            element = view_client.findViewById('com.simplemobiletools.contacts.pro:id/save')
            element.touch()
        except Exception as e:
            print("Exception: ", str(e))

        pass

    # delete contact
    def teardown(self, view_client):
        subprocess.run(["adb", "shell", "pm", "clear", "com.android.providers.contacts"])

    def check_finish(self, view_client, app_event) -> bool:
        # Check if the favorite button is clicked
        if app_event is not None:
            if app_event.type == AppEventType.Click and app_event.id_str == "com.simplemobiletools.contacts.pro:id/contact_toggle_favorite":
                return True
        return False
