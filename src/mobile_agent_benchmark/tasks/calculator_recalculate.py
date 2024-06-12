from ..bench_task import Task
from ..server import AppEvent, AppEventType

class CalculatorReCalculateTask(Task):
    def __init__(self, task_name="calculator_recalculate",
                 prompt="Calculate the result of '12 × 5'. However, during the input process, the number '4' was "
                        "mistakenly entered instead of '5'. Correct this by first enter 'C' to delete '4' and re-entering '5' and then perform the "
                        "calculation",
                 min_steps=3,
                 package="com.simplemobiletools.calculator",
                 max_steps=6,
                 stop_after_finish=True,
                 permissions=[]):
        super().__init__(task_name, prompt, min_steps, package, max_steps, stop_after_finish,permissions)

        self.text_filled = False
        self.last_event = None

    def setup(self, view_client):
        button_1 = view_client.findViewWithText('1')
        button_1.touch()

        button_2 = view_client.findViewWithText('2')
        button_2.touch()

        button_multiply = view_client.findViewWithText('×')
        button_multiply.touch()

        button_4 = view_client.findViewWithText('4')
        button_4.touch()

        view_client.dump()
        pass

    def check_finish(self, view_client, app_event: AppEvent) -> bool:
        result = view_client.findViewById('com.simplemobiletools.calculator:id/result')
        if result is not None and result.text().strip() == '60':
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

