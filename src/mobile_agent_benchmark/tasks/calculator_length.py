from ..bench_task import Task
from ..server import AppEvent, AppEventType


class CalculatorConvertLengthTask(Task):
    def __init__(self, task_name="calculator_convert_length",
                 prompt="Use Unit converter function to calculate how many kilometers 1mile is equal to",
                 min_steps=6,
                 package="com.simplemobiletools.calculator",
                 max_steps=12,
                 stop_after_finish=False,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish, permissions)

        self.mile_detected = False
        self.km_detected = False

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        mile = view_client.findViewWithText('Mile')
        kilometer = view_client.findViewWithText('Kilometer')
        mile_number = view_client.findViewWithText('1')
        kilometer_number = view_client.findViewWithText('1.609344')
        if mile is not None and kilometer is not None:
            if mile_number is not None and kilometer_number is not None:
                return True
        return False