from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class OpenNoteTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_open",
            prompt="open the note 'meeting'",
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
        def create_note(name,text):
            # Access the button to add a new note
            new_note_button = view_client.findViewById('com.simplemobiletools.notes.pro:id/new_note')
            new_note_button.touch()
            view_client.dump()

            title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/locked_note_title')
            title_view.type(name)
            
            save_button = view_client.findViewById('android:id/button1')
            save_button.touch()
            
            view_client.dump()

            text_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/text_note_view')
            text_view.type(text)
            view_client.dump()

        # Create example notes
        create_note("meeting","9pm May 5th 2024")
        create_note("Charles's secrets","I love you")
        create_note("to_do_list","Complete the task")
        
        pass    
    
    def check_finish(self, view_client, app_event):
        """
        Verify that specific notes have been deleted by checking their absence.
        """
        
        text_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/text_note_view')
        title_views = view_client.findViewWithText("9pm May 5th 2024")


        if  text_view.text() == "9pm May 5th 2024" and title_views is not None:
            return True
        return False
