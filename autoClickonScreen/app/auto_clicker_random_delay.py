import pyautogui
import time
import random
from utility.logger_util.setup_logger import logger


class AutoClicker:
    def __init__(self, max_wait_time=49):
        """
        @param max_wait_time: in seconds
        """
        self.click_position = None
        self.running = False
        self.max_wait_time = max_wait_time

    def process_user_request(self):
        self.capture_click_position()
        self.start_clicking()

    def capture_click_position(self, delay=10):
        """Waits for a few seconds and captures the current mouse position."""
        print(f"Move your mouse to the button you want to click. You have {delay} seconds...")
        time.sleep(delay)
        self.click_position = pyautogui.position()
        logger.info(f"Clicking will keep happening at: {self.click_position} until user presses Ctrl+C")

    def start_clicking(self, min_delay=5, max_delay=20):
        """Starts clicking at the captured position at random intervals."""
        if not self.click_position:
            logger.warning("Click position not set. Please run capture_click_position() first.")
            return

        self.running = True
        logger.info("Starting auto-clicker. Press Ctrl+C to stop.")
        try:
            while self.running:
                pyautogui.click(self.click_position)
                logger.info(f"Clicked at {self.click_position}")
                wait_time = random.randint(min_delay, max_delay)
                time.sleep(wait_time)
        except KeyboardInterrupt:
            self.stop_clicking()

    def stop_clicking(self):
        """Stops the clicking loop."""
        self.running = False
        logger.warning("Auto-clicker stopped by user.")

# if __name__ == "__main__":
#     clicker = AutoClicker()
#     clicker.capture_click_position()
#     clicker.start_clicking()
