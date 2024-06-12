from ..bench_task import Task
from ..server import AppEvent, AppEventType
import subprocess

class MessagerMakeConversationArchivedTask(Task):
    def __init__(self, task_name="messager_make_conversation_archived",
                 prompt="make the conversation with number '123456789' archived",
                 min_steps=3,
                 package="com.simplemobiletools.smsmessenger",
                 max_steps=6,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)
        self.moreOptionButtonClicked = False
        self.correctSelection = False
        self.alert_showed = False
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
        moreOptionButton = view_client.findViewWithContentDescription("More options")
        if moreOptionButton is None:
            return
        moreOptionButton.touch()
        view_client.dump()
        archiveButton = view_client.findViewWithText("Show archived conversations")
        archiveButton.touch()
        view_client.dump()
        archivedMessageView = view_client.findViewById("com.simplemobiletools.smsmessenger:id/conversation_address")
        while archivedMessageView is not None:
            archivedMessageView.longTouch()
            view_client.dump()
            deleteButton = view_client.findViewById("com.simplemobiletools.smsmessenger:id/cab_delete")
            deleteButton.touch()
            view_client.dump()
            YesButton = view_client.findViewWithText("Yes")
            YesButton.touch()
            view_client.dump()
            archivedMessageView = view_client.findViewById("com.simplemobiletools.smsmessenger:id/conversation_address")
        backButton = view_client.findViewWithContentDescription('Back')
        backButton.touch()
        view_client.dump()
        pass
    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        correctSelectionView = view_client.findViewById("com.simplemobiletools.smsmessenger:id/conversation_address")
        if correctSelectionView is not None:
            text = correctSelectionView.text()
            if text == '123456789':
                print('correct conversation selected')
                self.correctSelection = True
        
        moreOptionView = view_client.findViewWithText("Archive")
        if moreOptionView is not None:
            self.moreOptionButtonClicked = True
            print('detected more options button clicked')

        if view_client.findViewWithText('Are you sure you want to archive 1 conversation?') is not None:
            self.alert_showed = True

        if app_event is not None and app_event.package == 'com.simplemobiletools.smsmessenger':
            if app_event.type == AppEventType.Click:
                if len(app_event.text_list) == 1 and app_event.text_list[0] == 'Yes':
                    return self.correctSelection and self.alert_showed and self.moreOptionButtonClicked
          
        return False