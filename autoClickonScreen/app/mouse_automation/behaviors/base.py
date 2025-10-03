# Abstract base class for all mouse behaviors.
# All behaviors must implement the perform_action method.

from abc import ABC, abstractmethod
from utility.logger_util.setup_logger import logger

class MouseBehavior(ABC):
    @abstractmethod
    def perform_action(self):
        pass
