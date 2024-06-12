from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess

class MessagerAddBlockNumberTask(Task):
    def __init__(self, task_name="messager_add_block_numbers",
                 prompt="Add a number '123456789' to block list",
                 min_steps=5,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=10,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.okButtonClicked = False
        self.correctBlockNumberEntered = False
    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        return
    def teardown(self, view_client):
        print("teardown sms...")
        pkg = "com.simplemobiletools.smsmessenger"
        view_client.device.forceStop(package=pkg)
        view_client.device.startActivity(package=pkg)
        view_client.dump()
        settingsButton = view_client.findViewById('com.simplemobiletools.smsmessenger:id/settings')
        settingsButton.touch()
        view_client.dump()
        manageBlockedNumbersButton = view_client.findViewWithText('Manage blocked numbers')
        manageBlockedNumbersButton.touch()
        view_client.dump()
        numberSelection = view_client.findViewWithText('123456789')
        if numberSelection is not None:
            numberSelection.longTouch()
            view_client.dump()
            deleteButton = view_client.findViewWithContentDescription('Delete')
            deleteButton.touch()
            view_client.dump()
        pass
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        correctBlockNumberEntered = view_client.findViewWithText('123456789')
        if correctBlockNumberEntered is not None:
            self.correctBlockNumberEntered = True
            print('Correct block number entered')
        okButton = view_client.findViewWithText('OK')
        if okButton is None:
            self.okButtonClicked = True
            print('OK button clicked')
        activity_name = view_client.device.getTopActivityName()
        if 'ManageBlockedNumbersActivity' in activity_name:
            return self.correctBlockNumberEntered and self.okButtonClicked
        return False