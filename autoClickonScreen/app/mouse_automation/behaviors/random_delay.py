# Clicks at the current position with a random delay between actions.

from autoClickonScreen.app.mouse_automation.behaviors.base import MouseBehavior
import pyautogui
import time
import random

from utility.logger_util.setup_logger import logger

class RandomDelay(MouseBehavior):
    def perform_action(self):
        x, y = pyautogui.position()
        pyautogui.click(x, y)
        time.sleep(random.uniform(0.5, 2.0))
