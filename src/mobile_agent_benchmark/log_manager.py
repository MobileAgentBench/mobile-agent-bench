import os
from datetime import datetime
import numpy as np
import cv2
import json
from math import ceil

from .bench_task import Task, ActionLog

class LogManager():
    def __init__(self, log_dir) -> None:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        now = datetime.now()
        time_str = now.strftime("%Y_%m_%d-%H_%M_%S")
        self.log_dir = os.path.join(log_dir, time_str)
       
        os.makedirs(self.log_dir)

    def log_before_action(self, task: Task):
        log = ActionLog()
        log.begin_timestamp = datetime.timestamp(datetime.now())
        task.action_logs.append(log)
 
    def log_after_action(self, task: Task, time_stamp, action_desc: str, screenshot, step, model_input_text="", model_input_images=[], model_output_text=""):
        task_dir = os.path.join(self.log_dir, task.task_name)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        screenshot_dir = os.path.join(task_dir, 'screenshots')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        log = task.action_logs[-1]
        if log.step != -1:
            raise RuntimeError("Did you call `before_one_action`?")
        log.action = action_desc
        log.step = step
        log.end_timestamp = time_stamp
        log.input_tokens = self._count_text_tokens(model_input_text)
        for each in model_input_images:
            log.input_tokens += self._count_image_tokens(each.shape[1], each.shape[0])
        log.output_tokens = self._count_text_tokens(model_output_text)
        
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img_name = f"{step:04d}.png"
        img_path = os.path.join(screenshot_dir, img_name)
        cv2.imwrite(img_path, img)

        log.screenshot_path = img_path



    def save_log(self, task: Task):
        # TODO: introduce another int to store multiple runs for the same task
        task_dir = os.path.join(self.log_dir, task.task_name)
        if not os.path.exists(task_dir):
            os.makedirs(task_dir)
        json_dict = {
            'task': task.task_name,
            'prompt': task.prompt,
            'finished': task.finished,
            'stop_after_finish': task.stop_after_finish,
            'actions': []
        }

        for each_action in task.action_logs:
            action_dict = {
                'action': each_action.action,
                'step': each_action.step,
                'begin_timestamp': each_action.begin_timestamp,
                'end_timestamp': each_action.end_timestamp,
                'input_tokens': each_action.input_tokens,
                'output_tokens': each_action.output_tokens,
                'screenshot': each_action.screenshot_path
            }
            json_dict['actions'].append(action_dict)
        
        file_path = os.path.join(task_dir, f"{task.task_name}.json")
        with open(file_path, 'w') as file:
            # Convert the dictionary to a JSON string with pretty printing
            json.dump(json_dict, file, indent=4)

    def _count_text_tokens(self, text: str):
        return ceil(len(text) / 4)

    def _count_image_tokens(self, width: int, height: int):
        def resize(width, height):
            if width > 1024 or height > 1024:
                if width > height:
                    height = int(height * 1024 / width)
                    width = 1024
                else:
                    width = int(width * 1024 / height)
                    height = 1024
            return width, height
        width, height = resize(width, height)
        h = ceil(height / 512)
        w = ceil(width / 512)
        total = 85 + 170 * h * w
        return total

        