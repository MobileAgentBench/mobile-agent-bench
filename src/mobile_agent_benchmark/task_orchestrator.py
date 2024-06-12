from .server import AppEvent, start_server
from .tasks import *
from .log_manager import LogManager
from .bench_task import Task
import time
import queue
import subprocess
import json
import importlib.resources as pkg_resources
from com.dtmilano.android.viewclient import ViewClient
from datetime import datetime

class TaskOrchestrator():
    def __init__(self, log_dir='./', config_path=None):
        
        if config_path is None:
            config_path = pkg_resources.files("mobile_agent_benchmark") / "configs/default.json"
        with open(config_path) as f:
            config = json.load(f)

        tasks = []
        name_class_map = {}
        for clazz in Task.__subclasses__():
            task = clazz()
            name_class_map[task.task_name] = task
        for config_task in config["tasks"]:
            task = name_class_map[config_task["name"]]
            tasks.append(task)

        self.tasks = tasks

        self.current_task_id = 0
        self.current_task = None
        
        self.event_queue = queue.Queue()
    
        device, serialno = ViewClient.connectToDeviceOrExit()
        self.vc = ViewClient(device, serialno, useuiautomatorhelper=False)

        self.log_manager = LogManager(log_dir=log_dir)
        
        pass

    def _check_task_finish(self, view_client) -> bool:
        event = None
        finished = False
        if self.event_queue.empty():
            finished = self.current_task.check_finish(view_client, None)
           
        while not self.event_queue.empty():
            event = self.event_queue.get_nowait() # get also pops the element
            finished = self.current_task.check_finish(view_client, event)
            if finished:
                break
                
        print("-----------------------")
        print(f"Task Finished? {finished}")
        print("-----------------------")
        return finished



    def _on_receive_new_event(self, app_event):
        # this will be called from anohter thread
        # to ensure thread safety, we can only put an event into the queue
        # without calling `check_task_finish` function
        # in other words, 
        # app_event will not be delievered at the exact event happending time
        self.event_queue.put(app_event)

    # TODO: use `with` keyword
    def before_one_action(self):
        if self.current_task is None:
            return
        self.log_manager.log_before_action(self.current_task)


    def after_one_action(self, action_desc, agent_text_input="", agent_image_input=[], agent_text_output="") -> bool:
        """Inform the task orchestrator after one action is performed
        We can easily know the initial state, so we don't need `before_one_action`

        Args:
            action_desc (str): description of the action, e.g., `click`
            agent_text_input(str): text input to the model (to calculate cost)
            agent_image_input([np.ndarray]): image input to the model, OpenCV format (to calculate cost)
            agent_text_output(str): model output (to calculate cost)

        Returns:
            bool: agent should stop (exceed max steps or finished)
        """
        if self.current_task is None:
            return False
        timestamp = datetime.timestamp(datetime.now())
        self.current_task.current_step += 1

        # sleep is important here. Because when we run adb commands (dump)
        # accessibility callback doesn't work
        # we may lose some action events
        time.sleep(1)
        self.vc.dump() # update state

        screenshot = self.vc.device.takeSnapshot(reconnect=True)
        # TODO: calculate LLM cost
        self.log_manager.log_after_action(self.current_task, timestamp,
                                          action_desc, screenshot, 
                                          self.current_task.current_step, 
                                          model_input_text=agent_text_input, 
                                          model_input_images=agent_image_input, 
                                          model_output_text=agent_text_output)
        
        
        should_stop = False

        if self.current_task.current_step > self.current_task.max_steps:
           should_stop = True
        
        if not self.current_task.finished:
            # once a task is finished, it's always finsihed
            self.current_task.finished = self._check_task_finish(self.vc)

        if self.current_task.stop_after_finish and self.current_task.finished:
            should_stop = True
        
        return should_stop
    
    
    def run(self, agent_fn):
        start_server(self._on_receive_new_event)
        time.sleep(1)

        for i in range(len(self.tasks)):
            self.current_task_id = i
            self.current_task = self.tasks[i]

            print(f"==== Running: {self.current_task.prompt} ====")

            self.vc.device.forceStop(package=self.current_task.package)
            subprocess.run(["adb", "shell", "pm", "clear", self.current_task.package]) # deletes all data to restore app state
            # grant permission
            for each in self.current_task.permissions:
                subprocess.run(["adb", "shell", "pm", "grant", self.current_task.package, each])
            self.vc.device.startActivity(package=self.current_task.package)

            # setup
            self.vc.dump()
            self.current_task.setup(self.vc)
            time.sleep(1) # wait for pending events
            with self.event_queue.mutex: # clear events caused by setup
                self.event_queue.queue.clear()

            # log initial state
            self.vc.dump() # update state
            screenshot = self.vc.device.takeSnapshot(reconnect=True)
            self.log_manager.log_before_action(self.current_task)
            self.log_manager.log_after_action(self.current_task, 0, "init", screenshot, 0)

            # should not run in another thread / process
            agent_fn(self.current_task.prompt)

            # when the agent thinks it's done, we still need to wait for events
            # for example, the agent click a button and exit
            # we need to wait for a bit to make sure the event is received
            time.sleep(1)
            while not self.event_queue.empty:
                print("send pending events...")
                self.vc.dump()
                if not self.current_task.finished:
                    self.current_task.finished = self._check_task_finish(self.vc)

            self.log_manager.save_log(self.current_task)

            # teardown
            self.vc.dump()
            self.current_task.teardown(self.vc)
            subprocess.run(["adb", "shell", "pm", "clear", self.current_task.package]) # delete all data one more time to tear down

           





