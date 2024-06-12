from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class RenameNoteTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_rename",
            prompt="rename the current note to 'finished_task'",
            min_steps=5,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=10, 
            stop_after_finish=False,
            permissions=[]
        )
        self.search = False
        self.content = False

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
        create_note("unfinished_task","Undo")
    

    def check_finish(self, view_client, app_event):
        text_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/text_note_view')
        title_view = view_client.findViewWithText('finished_task')

        if text_view is not None and title_view is not None:
            return text_view.text() == "Undo" and title_view.map['class'] == 'android.widget.TextView'

        return False
