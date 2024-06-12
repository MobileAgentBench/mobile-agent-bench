from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess
from .messager_start_a_conversation import MessagerStartConversationTask
from .messager_check_message_properties import MessagerCheckMessagePropertiesTask

class MessagerCreateConversationAndSawMessagePropertiesTask(Task):
    def __init__(self, task_name="messager_create_conversation_and_check_message_properties",
                 prompt="start a conversation with number '123456789', send a message 'i luv u', and check for message properties ",
                 min_steps=8,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=16,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.createTask = MessagerStartConversationTask()
        self.checkTask = MessagerCheckMessagePropertiesTask()
        self.createTaskFinished = False
        
    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        return
    def teardown(self, view_client):
        self.checkTask.teardown(view_client)
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if not self.createTaskFinished:
            self.createTaskFinished = self.createTask.check_finish(view_client, app_event)
        else:
            print("create finished, checking properties")
            return self.checkTask.check_finish(view_client, app_event)
        return False