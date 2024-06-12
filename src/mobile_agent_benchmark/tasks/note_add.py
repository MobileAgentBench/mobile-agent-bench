from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType


class OpenNoteTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_add",
            prompt="add a new note named 'TODO List'",
            min_steps=3,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=6, 
            stop_after_finish=False,
            permissions=[]
        )
        self.last_event = None

    def check_finish(self, view_client, app_event) -> bool:
        """
        Check if a note named 'to_do_list' is currently open by identifying the presence of the EditText for note text and verifying the text content.
        """
        title = view_client.findViewWithText("TODO List")
        if title is not None:
            if title.map['class'] == "android.widget.TextView":
                # if typed elsewhere, it will be EditTextView
                return True
        return False
