from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess
from . import task_utils

class MessagerStartConversationTask(Task):
    def __init__(self, task_name="messager_start_a_conversation",
                 prompt="start a conversation with number '123456789', and send a message 'i luv u'",
                 min_steps=8,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=16,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.contactAddressCorrect = False
        
    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        return
      
    def teardown(self, view_client):
        task_utils.messager_delete_all(view_client)

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        # check if the conversation is started
        contactView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/new_conversation_address')
        if contactView is not None :
            text = contactView.text()
            if text == '123456789':
                self.contactAddressCorrect = True
                print('contact address correct')
        messageView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/thread_message_body')
        if messageView is not None:
            text = messageView.text()
            if text.lower() == 'i luv u':
                print('message correct')
                return self.contactAddressCorrect
        return False