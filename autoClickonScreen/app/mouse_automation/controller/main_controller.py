# MainController is responsible for orchestrating the automation.
# It loads the selected behavior and repeatedly performs the action.
import time

from autoClickonScreen.app.mouse_automation.factory.behavior_factory import BehaviorFactory
from autoClickonScreen import config
from utility.logger_util.setup_logger import logger

class MainController:
    def __init__(self,
                 max_idle_time: int=config.DEFAULT_MAX_IDLE_TIME,
                 app_behavior: str=config.DEFAULT_BEHAVIOR):
        """
        :param app_behavior: Available options are following:
                "default_click", "smooth_movement", "random_delay",
                "jitter_movement", "idle_behavior", "breaks_and_pauses"

        :param max_idle_time: in seconds
        """
        # Load the behavior based on user preference
        self.max_idle_time = max_idle_time

        #
        self.behavior = BehaviorFactory.get_behavior(name=app_behavior)
        self.running = False

    def stop_clicking(self):
        """Stops the clicking loop."""
        self.running = False
        logger.warning("Auto-clicker stopped by user.")

    def run(self):
        # Continuously perform the selected behavior

        self.running = True
        logger.info("Starting auto-clicker. Press Ctrl+C to stop.")

        try:
            while self.running:
                self.behavior.perform_action()
                if self.max_idle_time:
                    time.sleep(self.max_idle_time)

        except KeyboardInterrupt:
            self.stop_clicking()

