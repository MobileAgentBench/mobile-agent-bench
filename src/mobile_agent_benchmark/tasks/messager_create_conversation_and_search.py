from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess
from .messager_start_a_conversation import MessagerStartConversationTask
from .messager_search_contacts import MessagerSearchContactsTask
from . import task_utils

class MessagerCreateConversationAndSearchTask(Task):
    def __init__(self, task_name="messager_create_conversation_and_search",
                 prompt="start a conversation with number '123456789', and send a message 'i luv u', back to the main page and search for the contact '123456789'",
                 min_steps=8,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=16,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.createTask = MessagerStartConversationTask()
        self.searchTask = MessagerSearchContactsTask()
        self.createTaskFinished = False
        
    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        return
    
    def teardown(self, view_client):
        task_utils.messager_delete_all(view_client)
        
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        if not self.createTaskFinished:
            self.createTaskFinished = self.createTask.check_finish(view_client, app_event)
        else:
            print("create finished, checking search")
            return self.searchTask.check_finish(view_client, app_event)
        return False