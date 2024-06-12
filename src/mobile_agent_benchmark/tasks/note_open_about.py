from ..bench_task import Task
from com.dtmilano.android.viewclient import ViewClient

class OpenAboutTask(Task):
    def __init__(self):
        super().__init__(
            task_name="note_open_about",
            prompt="open about page",
            min_steps=2,  
            package="com.simplemobiletools.notes.pro",  
            max_steps=4, 
            stop_after_finish=False,
            permissions=[]
        )
    def check_finish(self, view_client, app_event) -> bool:
        activity_name = self.get_top_activity_name()
        if 'AboutActivity' in activity_name:
            return True
        return False