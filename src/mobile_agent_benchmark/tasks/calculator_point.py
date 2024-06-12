from ..bench_task import Task
from ..server import AppEvent, AppEventType

class CalculatorPointTask(Task):
    def __init__(self, task_name="calculator_point",
                 prompt="Calculate the result of '19.7 - 81.3'",
                 min_steps=10,
                 package="com.simplemobiletools.calculator",
                 max_steps=20,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.text_filled = False
        self.last_event = None

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        result = view_client.findViewById('com.simplemobiletools.calculator:id/result')
        if result is not None and result.text().strip() == '-61.6':
            self.text_filled = True

        if app_event is not None and app_event.package == self.package:
            # last step is =
            if app_event.type == AppEventType.Click and len(app_event.text_list) == 1 and \
                    app_event.text_list[0] == '=':
                if self.last_event is not None and self.last_event.type == AppEventType.Click and len(
                        self.last_event.text_list) == 1:
                    return self.text_filled
            self.last_event = app_event
        return False

