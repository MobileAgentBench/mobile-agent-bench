from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class DeleteNoteTask(Task):
     def __init__(self):
         super().__init__(
             task_name="note_delete",
             prompt="delete the 'to_do_list' and 'meeting' note",
             min_steps=4,  
             package="com.simplemobiletools.notes.pro",  
             max_steps=8, 
             stop_after_finish=False,
             permissions=[]
         )

     def setup(self, view_client):
         """
         Prepares the environment by creating a set of notes that will be manipulated during the task.
         This includes interacting with the UI to input the note details and confirm their creation.
         """
         def create_note(name):
             # Access the button to add a new note
             new_note_button = view_client.findViewById('com.simplemobiletools.notes.pro:id/new_note')
             new_note_button.touch()
             view_client.dump()

             title_view = view_client.findViewById('com.simplemobiletools.notes.pro:id/locked_note_title')
             title_view.type(name)

             save_button = view_client.findViewById('android:id/button1')
             save_button.touch()

             view_client.dump()

         # Create example notes
         create_note("work_list")
         create_note("to_do_list")
         create_note("meeting")
         pass


     def check_finish(self, view_client, app_event):
         """
         Verify that specific notes have been deleted by checking their absence.
         """

         work_list = view_client.findViewWithText("work_list")
         to_do_list = view_client.findViewWithText("to_do_list")
         meeting = view_client.findViewWithText("meeting")


         if work_list is not None and to_do_list is None and meeting is None:
             return True
         return False