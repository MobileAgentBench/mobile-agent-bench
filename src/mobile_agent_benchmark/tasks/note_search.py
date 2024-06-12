from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class SearchNoteTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_search",
            prompt="search 'secret' in note 'Charles's secrets'",
            min_steps=2,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=4, 
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
            title_view.setText(name)
            view_client.dump()
            
            save_button = view_client.findViewWithText('OK')
            save_button.touch()
            view_client.dump()
            
            text_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/text_note_view')
            text_view.setText(text)
            view_client.dump()

        # Create example notes
        create_note("Charles's secrets","The secret is I love you")
        pass
    
    
    
    def check_finish(self, view_client, app_event) -> bool:
        
        
        search_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/search_query')
        if search_view is not None:
            if search_view.text().lower() == 'secret':
                self.search = True
            
        note_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/text_note_view')
        if note_view is not None:
            note_string = note_view.text()
            if 'secret' in note_string.lower():
                self.content = True
            return self.search and self.content
    
