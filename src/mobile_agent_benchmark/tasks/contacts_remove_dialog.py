from ..bench_task import Task
from ..server import AppEvent, AppEventType

class ContactsRemoveDialog(Task):
    def __init__(self, task_name="contacts_remove_dialog",
                 prompt="Remove the dialog button, and then return to the main view",
                 min_steps=4,
                 package="com.simplemobiletools.contacts.pro",
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=["android.permission.READ_CONTACTS"]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.dialog = False
        self.add = False

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        # make sure can found add button on main view
        add_button = view_client.findViewById('com.simplemobiletools.contacts.pro:id/fragment_fab')
        if add_button is not None:
            self.add = True
            # make sure cannot found dialog button on main view
            dialog_buuton = view_client.findViewById('com.simplemobiletools.contacts.pro:id/main_dialpad_button')
            if dialog_buuton is None:
                self.dialog = True
        return self.dialog and self.add