"""Module that defines the PictorDrawable interface."""

from abc import ABC, abstractmethod
from PIL import ImageDraw


# pylint: disable=too-few-public-methods
class PictorDrawable(ABC):
    """Drawable interface."""

    @abstractmethod
    def draw(self, draw: ImageDraw.Draw):
        """Interface method to draw on given ImageDraw.Draw object."""
