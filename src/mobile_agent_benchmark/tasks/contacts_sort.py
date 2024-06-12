import subprocess

from ..bench_task import Task
from ..server import AppEvent, AppEventType

class ContactsSort(Task):
    def __init__(self, task_name="contacts_sort",
                 prompt="Sort contacts by Data created time, Descending",
                 min_steps=5,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.yuzai = False
        self.zack = False

    # create contact yuzai
    def setup(self, view_client):
        button_add = view_client.findViewById('com.simplemobiletools.contacts.pro:id/fragment_fab')
        button_add.touch()

        view_client.dump()

        try:
            element = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_first_name')
            element.touch()

            view_client.device.type('Yuzai')
        except Exception as e:
            print("ExceptionName: ", str(e))

        try:
            element = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_number')
            element.setText('123456789')
        except Exception as e:
            print("ExceptionNumber: ", str(e))

        try:
            element = view_client.findViewById('com.simplemobiletools.contacts.pro:id/save')
            element.touch()
        except Exception as e:
            print("Exception: ", str(e))

        view_client.dump()

        view_client.sleep(1)

        button_add = view_client.findViewById('com.simplemobiletools.contacts.pro:id/fragment_fab')
        button_add.touch()

        view_client.dump()

        try:
            element = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_first_name')
            element.touch()

            view_client.device.type('Zack')
        except Exception as e:
            print("ExceptionName: ", str(e))

        try:
            element = view_client.findViewByIdOrRaise('com.simplemobiletools.contacts.pro:id/contact_number')
            element.setText('123456789')
        except Exception as e:
            print("ExceptionNumber: ", str(e))

        try:
            element = view_client.findViewById('com.simplemobiletools.contacts.pro:id/save')
            element.touch()
        except Exception as e:
            print("Exception: ", str(e))

        view_client.dump()

        pass

    # delete contact Yuzai
    def teardown(self, view_client):
        subprocess.run(["adb", "shell", "pm", "clear", "com.android.providers.contacts"])

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        sorted_name = ["zack", "yuzai"]
        current = 0
        try:
            # If there is no contact, return False
            recycler_view = view_client.findViewById("com.simplemobiletools.contacts.pro:id/fragment_list")
            if recycler_view is not None:
                # The List should be ['Zack', 'Yuzai']
                child_zack = recycler_view.children[0]
                if (child_zack['class'] == 'android.view.ViewGroup'
                        and child_zack['resource-id'] == 'com.simplemobiletools.contacts.pro:id/item_contact_frame'):
                    for subchild in child_zack.children:
                        if subchild['class'] == 'android.widget.TextView':
                            contact_name = subchild.getText()
                            print("current contact name: ", contact_name)
                            if contact_name.lower() == "zack":
                                self.zack = True
                child_yuzai = recycler_view.children[1]
                if (child_yuzai['class'] == 'android.view.ViewGroup'
                        and child_yuzai['resource-id'] == 'com.simplemobiletools.contacts.pro:id/item_contact_frame'):
                    for subchild in child_yuzai.children:
                        if subchild['class'] == 'android.widget.TextView':
                            contact_name = subchild.getText()
                            print("current contact name: ", contact_name)
                            if contact_name.lower() == "yuzai":
                                self.yuzai = True

            return self.yuzai and self.zack
        except Exception as e:
            print(f"Exception: {str(e)}")
            return False