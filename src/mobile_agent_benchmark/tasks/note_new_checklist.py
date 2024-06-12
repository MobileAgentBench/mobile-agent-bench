from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType


class ChecklistTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_new_checklist",
            prompt="add a new Checklist named 'TODO List'",
            min_steps=4,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=8, 
            stop_after_finish=False,
            permissions=[]
        )
        self.clicked_checklist = False
        self.clicked_text = False
    def check_finish(self, view_client, app_event) -> bool:
        """
        Check if a note named 'to_do_list' is currently open by identifying the presence of the EditText for note text and verifying the text content.
        """

        if app_event is not None:
            if app_event.type == AppEventType.Click:
                if 'Checklist' in app_event.text_list:
                    self.clicked_checklist = True
                    self.clicked_text = False
                elif 'Text note' in app_event.text_list:
                    self.clicked_text = True
                    self.clicked_checklist = False

        title_views = view_client.findViewWithText('TODO List')
        if title_views.map['class'] == "android.widget.TextView":
            return self.clicked_checklist and (not self.clicked_text)
        return False
