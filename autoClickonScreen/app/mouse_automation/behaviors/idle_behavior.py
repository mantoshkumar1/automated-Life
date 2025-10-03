# Occasionally pauses to simulate idle or distracted behavior.

from autoClickonScreen.app.mouse_automation.behaviors.base import MouseBehavior
import pyautogui
import time
import random

from utility.logger_util.setup_logger import logger

class IdleBehavior(MouseBehavior):
    def perform_action(self):
        if random.random() < 0.3:
            # Simulate idle time
            time.sleep(random.uniform(2, 5))
        else:
            x, y = pyautogui.position()
            pyautogui.click(x, y)
        time.sleep(1)
