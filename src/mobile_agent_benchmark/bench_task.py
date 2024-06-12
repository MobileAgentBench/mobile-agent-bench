from com.dtmilano.android.viewclient import ViewClient
import subprocess
import re

class ActionLog:
    def __init__(self):
        self.action = ''
        self.step = -1
        self.begin_timestamp = 0
        self.end_timestamp = 0
        self.screenshot_path = ''
        self.input_tokens = 0
        self.output_tokens = 0

class Task(object):
    def __init__(self, task_name, prompt, min_steps, package, max_steps=20, stop_after_finish=False, permissions=[]):
        self.task_name = task_name
        self.prompt = prompt
        self.min_steps = min_steps
        self.package = package
        self.max_steps = max_steps
        self.stop_after_finish = stop_after_finish
        self.permissions = permissions

        self.current_step = 0
        self.action_logs = []

        self.finished = False

    def get_top_activity_name(self, timeout=60) -> str:
        """get top activiy name with timeout
        When you call view_client getTopActivityName, 
        you may get a wrong one, this is because the default timeout is too short

        Args:
            timeout (int, optional): timeout. Defaults to 60.

        Returns:
            str: the top
        """
        output = subprocess.run(["adb", "shell", "dumpsys", "-t", str(timeout), "activity", "top"], capture_output=True, text=True)
        activity_re = re.compile('\s*ACTIVITY ([A-Za-z0-9_.]+)/([A-Za-z0-9_.\$]+) \w+ pid=(\d+)')
        m = activity_re.findall(output.stdout)
        if len(m) > 0:
            activity_and_pid = m[-1]
            return activity_and_pid[0] + '/' + activity_and_pid[1]
        else:
            return None


    def setup(self, view_client):
        """Setup the task execution environment, either with adb or UI automation
        """
        return
    
    def teardown(self, view_client):
        """Restore environment
        """
        return

    def check_finish(self, view_client, app_event) -> bool:
        raise NotImplementedError
    


        
