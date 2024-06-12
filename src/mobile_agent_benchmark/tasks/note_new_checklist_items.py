from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient
from ..server import AppEvent, AppEventType

class ChecklistItemTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_new_checklist_items",
            prompt="create a checklist named 'Shopping list' and add an item named 'Milk'",
            min_steps=7,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=14, 
            stop_after_finish=False,
            permissions=[]
        )
        self.last_event = None
        self.checklist = False


    def check_finish(self, view_client, app_event):
        """
        Verify that specific notes have been deleted by checking their absence.
        """
        
        title_view = view_client.findViewWithText('Shopping list')
        text_view = view_client.findViewWithText('Milk')
        
        if title_view is not None and text_view is not None:
            if title_view.map['class'] == 'android.widget.TextView' \
                and text_view.map['resource-id'] == 'com.simplemobiletools.notes.pro:id/checklist_title':
                return True
        return False
            
            
            
            
            
            