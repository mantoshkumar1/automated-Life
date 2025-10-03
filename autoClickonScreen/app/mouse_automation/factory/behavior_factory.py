# Factory class to return the appropriate behavior based on a string key.

from autoClickonScreen.app.mouse_automation.behaviors.default_click import DefaultClickBehavior
from autoClickonScreen.app.mouse_automation.behaviors.smooth_movement import SmoothMovement
from autoClickonScreen.app.mouse_automation.behaviors.random_delay import RandomDelay
from autoClickonScreen.app.mouse_automation.behaviors.jitter_movement import JitterMovement
from autoClickonScreen.app.mouse_automation.behaviors.idle_behavior import IdleBehavior
from autoClickonScreen.app.mouse_automation.behaviors.breaks_and_pauses import BreaksAndPauses

from utility.logger_util.setup_logger import logger

class BehaviorFactory:
    @staticmethod
    def get_behavior(name: str):
        # Map behavior names to their corresponding classes
        behaviors = {
            "default_click": DefaultClickBehavior,
            "smooth_movement": SmoothMovement,
            "random_delay": RandomDelay,
            "jitter_movement": JitterMovement,
            "idle_behavior": IdleBehavior,
            "breaks_and_pauses": BreaksAndPauses,
        }
        # Return the selected behavior or default if not found
        return behaviors.get(name, DefaultClickBehavior)()
