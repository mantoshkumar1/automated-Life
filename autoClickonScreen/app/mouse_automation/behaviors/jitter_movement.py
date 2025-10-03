# Simulates small, random jitter movements before clicking.

from autoClickonScreen.app.mouse_automation.behaviors.base import MouseBehavior
import pyautogui
import time
import random

from utility.logger_util.setup_logger import logger

class JitterMovement(MouseBehavior):
    def perform_action(self):
        x, y = pyautogui.position()
        for _ in range(5):
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            pyautogui.moveRel(dx, dy, duration=0.05)
        pyautogui.click()
        time.sleep(1)
