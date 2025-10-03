# Default behavior: clicks at the current mouse position every second.

from autoClickonScreen.app.mouse_automation.behaviors.base import MouseBehavior
import pyautogui
import time

from utility.logger_util.setup_logger import logger

class DefaultClickBehavior(MouseBehavior):
    def perform_action(self):
        x, y = pyautogui.position()
        pyautogui.click(x, y)
        time.sleep(1)
