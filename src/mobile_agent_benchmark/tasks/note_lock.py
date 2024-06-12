import subprocess

from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType


# from .note_new_checklist import

class NoteLockTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_lock",
            prompt="use the pin '2580' to open the locked note 'password_list'",
            min_steps=6,
            package="com.simplemobiletools.notes.pro",
            max_steps=12,
            stop_after_finish=False,
            permissions=[]
        )

    def setup(self, view_client):
        def enter_pin(pin):
            for digit in pin:
                # Find the button for the current digit
                pin_button_id = f'com.simplemobiletools.notes.pro:id/pin_{digit}'
                pin_button = view_client.findViewById(pin_button_id)
                if pin_button:
                    pin_button.touch()
                    view_client.dump()
                else:
                    raise ValueError(f"Pin button for digit '{digit}' not found.")
            save_button = view_client.findViewById('com.simplemobiletools.notes.pro:id/pin_ok')
            save_button.touch()
            view_client.dump()

        def open_lock(pin):
            moreOptionButton = view_client.findViewWithContentDescription('More options')
            moreOptionButton.touch()

            view_client.dump()

            # touch 'Lock note' button
            delete_button = view_client.findViewWithText('Lock note')
            delete_button.touch()

            view_client.dump()

            # touch 'ok'
            ok_button = view_client.findViewById('android:id/button1')
            ok_button.touch()

            view_client.dump()

            # touch 'PIN' button
            delete_button = view_client.findViewWithText('PIN')
            delete_button.touch()
            view_client.dump()

            enter_pin(pin)

            # one more time for confirmation
            enter_pin(pin)

        def create_checklist(name, item1):
            # Access the button to add a new note
            new_note_button = view_client.findViewById('com.simplemobiletools.notes.pro:id/new_note')
            new_note_button.touch()
            view_client.dump()

            type_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/type_checklist')
            type_view.touch()

            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/locked_note_title')
            title_view.type(name)

            save_button = view_client.findViewById('android:id/button1')
            save_button.touch()

            view_client.dump()

            # input item1
            check_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/checklist_fab')
            check_view.touch()
            view_client.dump()

            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/title_edit_text')
            title_view.type(item1)

            save_button2 = view_client.findViewById('android:id/button1')
            save_button2.touch()
            view_client.dump()

        def add_text(text):
            text_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/text_note_view')
            text_view.type(text)
            view_client.dump()

        create_checklist("password_list","unique2580")

        open_lock("2580")
        check_button = view_client.findViewWithText('password_list')
        check_button.touch()

        view_client.dump()

        # Return to the main page and come back to note page

        subprocess.run(["adb", "shell", "input", "keyevent", "3"])

        view_client.dump()

        subprocess.run(["adb", "shell", "monkey", "-p", "com.simplemobiletools.notes.pro", "-c", "android.intent.category.LAUNCHER", "1"])

        view_client.dump()

        pass

    def check_finish(self, view_client, app_event) -> bool:
        note = view_client.findViewWithText("unique2580")
        if note is not None:
            return True
        return False
