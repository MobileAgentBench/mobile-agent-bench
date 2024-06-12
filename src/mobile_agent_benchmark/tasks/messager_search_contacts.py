from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess
from . import task_utils

class MessagerSearchContactsTask(Task):
    def __init__(self, task_name="messager_search_contacts",
                 prompt="search for the contact '123456789' at top search bar",
                 min_steps=2,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=4,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.contactAddressCorrect = False
        
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
        pass
    
    def teardown(self, view_client):
        task_utils.messager_delete_all(view_client)
        
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        # check if the correct contact is entered into the searchbox
        searchView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/top_toolbar_search')
        if searchView is not None:
            text = searchView.text()
            if text == '123456789':
                self.contactAddressCorrect = True
                print('correctly entered')
        contactView = view_client.findViewById('com.simplemobiletools.smsmessenger:id/conversation_address')
        if contactView is not None:
            text = contactView.text()
            if text == '123456789':
                return self.contactAddressCorrect
        return False