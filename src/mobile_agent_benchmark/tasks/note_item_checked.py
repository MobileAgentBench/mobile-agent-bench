from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType
class NoteItemCheck(Task):
    def __init__(self):
        super().__init__(
            task_name="note_item_checked",
            prompt="Check the item 'eggs' for shopping_list",
            min_steps=1,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=2, 
            stop_after_finish=False,
            permissions=[]
        )
    def setup(self, view_client):
        """
        Prepares the environment by creating a set of notes that will be manipulated during the task.
        This includes interacting with the UI to input the note details and confirm their creation.
        """
        def create_note(name,item1,item2,item3):
            # Access the button to add a new note
            new_note_button = view_client.findViewById('com.simplemobiletools.notes.pro:id/new_note')
            new_note_button.touch()
            view_client.dump()
            
            type_view = view_client.findViewWithText('Checklist')
            type_view.touch()
            
            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/locked_note_title')
            title_view.type(name)
            
            save_button = view_client.findViewById('android:id/button1')
            save_button.touch()
            
            view_client.dump()
            
            
            #input item1
            check_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/checklist_fab')
            check_view.touch()
            view_client.dump()
            
            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/title_edit_text')
            title_view.type(item1)
            
            save_button2 = view_client.findViewById('android:id/button1')
            save_button2.touch()
            view_client.dump()
            
            
            #input item2
            check_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/checklist_fab')
            check_view.touch()
            view_client.dump()
            
            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/title_edit_text')
            title_view.type(item2)
            
            save_button2 = view_client.findViewById('android:id/button1')
            save_button2.touch()
            view_client.dump()
            
            
            #input item3
            check_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/checklist_fab')
            check_view.touch()
            view_client.dump()
            
            
            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/title_edit_text')
            title_view.type(item3)
            
            save_button2 = view_client.findViewById('android:id/button1')
            save_button2.touch()
            view_client.dump()
        create_note("shopping_list","eggs","beer","steak")
        pass
        
        #Do I need to create two checklist to do further task
    def check_finish(self, view_client, app_event) -> bool:
        if app_event is not None:
            if app_event.type == AppEventType.Click and 'eggs' in app_event.text_list:
                return True
        return False
    