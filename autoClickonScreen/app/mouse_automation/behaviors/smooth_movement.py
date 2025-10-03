# Moves the mouse smoothly to a nearby random location and clicks.

from autoClickonScreen.app.mouse_automation.behaviors.base import MouseBehavior
import pyautogui
import time
import random

from utility.logger_util.setup_logger import logger

class SmoothMovement(MouseBehavior):
    def perform_action(self):
        x, y = pyautogui.position()
        new_x = x + random.randint(-100, 100)
        new_y = y + random.randint(-100, 100)
        pyautogui.moveTo(new_x, new_y, duration=random.uniform(0.5, 1.5))
        pyautogui.click()
        time.sleep(1)
