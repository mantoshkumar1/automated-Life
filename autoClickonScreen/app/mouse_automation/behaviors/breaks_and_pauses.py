# Takes a longer break after every 10 actions to simulate human rest.
from autoClickonScreen.app.mouse_automation.behaviors.base import MouseBehavior
import pyautogui
import time
import random

from utility.logger_util.setup_logger import logger

class BreaksAndPauses(MouseBehavior):
    def __init__(self):
        self.counter = 0

    def perform_action(self):
        self.counter += 1
        if self.counter % 10 == 0:
            # Simulate a break
            time.sleep(random.uniform(5, 10))
        x, y = pyautogui.position()
        pyautogui.click(x, y)
        time.sleep(1)
