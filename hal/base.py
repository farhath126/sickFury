from abc import ABC, abstractmethod
from typing import List
from PIL import Image

class DisplayDriver(ABC):
    @abstractmethod
    def init(self):
        """Initialize the display hardware/window."""
        pass

    @abstractmethod
    def draw_image(self, image: Image.Image):
        """Render a PIL Image to the screen."""
        pass

    @abstractmethod
    def clear(self):
        """Clear the display."""
        pass

class InputDriver(ABC):
    @abstractmethod
    def init(self):
        """Initialize input hardware."""
        pass

    @abstractmethod
    def get_events(self) -> List[str]:
        """Return a list of mapped event strings (from core.events)."""
        pass
