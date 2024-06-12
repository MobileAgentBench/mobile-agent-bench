from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess
from . import task_utils

class MessagerCheckMessagePropertiesTask(Task):
    def __init__(self, task_name="messager_check_message_properties",
                 prompt="open the conversation with contact number '123456789', and check for a random message's properties ",
                 min_steps=4,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=8,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.receiverCorrect = False
        
    def setup(self, view_client):
        subprocess.run(["adb","shell","pm", "disable-user", "--user", "0", "com.google.android.apps.messaging"])
        addConversationButton = view_client.findViewById("com.simplemobiletools.smsmessenger:id/conversations_fab")
        addConversationButton.touch()
        view_client.dump()
        setContactButton = view_client.findViewById("com.simplemobiletools.smsmessenger:id/new_conversation_address")
        setContactButton.setText("123456789")
        view_client.dump()
        addButton = view_client.findViewById("com.simplemobiletools.smsmessenger:id/new_conversation_confirm")
        addButton.touch()
        view_client.dump()
        editMessage = view_client.findViewById("com.simplemobiletools.smsmessenger:id/thread_type_message")
        editMessage.setText("i luv u")
        view_client.dump()
        sendButton = view_client.findViewById("com.simplemobiletools.smsmessenger:id/thread_send_message")
        sendButton.touch()
        view_client.dump()
        backButton = view_client.findViewWithContentDescription('Back')
        backButton.touch()
        view_client.dump()
        sndBackButton = view_client.findViewWithContentDescription('Back')
        sndBackButton.touch()
        view_client.dump()
        return
    
    def teardown(self, view_client):
        print("teardown sms...")
        task_utils.messager_delete_all(view_client)
    
    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None and app_event.package == 'com.simplemobiletools.smsmessenger':
            if app_event.type == AppEventType.WindowStateChange:
                if len(app_event.text_list) == 6 and app_event.text_list[0] == 'Message details' and app_event.text_list[2] == '123456789':
                    return True
        return False