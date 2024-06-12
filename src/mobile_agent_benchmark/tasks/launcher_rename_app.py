from ..bench_task import Task
from ..server import AppEvent, AppEventType
from . import task_utils


class LauncherRenameApp(Task):
    def __init__(
        self,
        task_name="launcher_rename_app",
        prompt="Rename Chrome in Launcher to MyChrome",
        min_steps=5,
        package="com.simplemobiletools.applauncher",
        max_steps=10,
        stop_after_finish=False,
        permissions=[],
    ):
        super().__init__(
            task_name,
            prompt,
            min_steps,
            package,
            max_steps,
            stop_after_finish,
            permissions,
        )

        self.at_home = False

    # Add Apps
    def setup(self, view_client):
        # touch '+' button
        button_add = view_client.findViewById(
            "com.simplemobiletools.applauncher:id/fab"
        )
        button_add.touch()

        view_client.dump()

        # Select Chrome
        try:
            element = view_client.findViewWithText("Chrome")
            if not element.checked():
                element.touch()

        except Exception as e:
            print("ExceptionFindAppChrome: ", str(e))

        # Select Camera
        try:
            element = view_client.findViewWithText("Camera")
            if not element.checked():
                element.touch()
        except Exception as e:
            print("ExceptionFindAppCamera: ", str(e))

        # click save button
        try:
            element = view_client.findViewById("android:id/button1")
            element.touch()
        except Exception as e:
            print("Exception: ", str(e))

        pass

    def check_finish(self, view_client, app_event) -> bool:
        # Check if at the main view
        launcher_home = view_client.findViewById(
            "com.simplemobiletools.applauncher:id/coordinator_layout"
        )
        if launcher_home is not None:
            self.at_home = True

        chrome_view = view_client.findViewWithText("MyChrome")
        if chrome_view is not None and self.at_home:
            return True

        self.at_home = False
        return False
