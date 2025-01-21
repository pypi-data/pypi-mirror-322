"""Module that defines the PictorRectangle class."""

from PIL import ImageDraw
from src.pictor_lib.pictor_box import PictorBox
from src.pictor_lib.pictor_drawable import PictorDrawable


@dataclass
class PictorRectangleStyle:
    """Style parameter for rectangle."""

    fill_color: str = None
    outline_color: str = None
    outline_width: int = 1

    def copy(self) -> 'PictorRectangleStyle':
        """Create a new instance by copying all fields."""

        return PictorRectangleStyle(fill_color=self.fill_color,
                                    outline_color=self.outline_color,
                                    outline_width=self.outline_width)


@dataclass
class PictorRectangle(PictorDrawable):
    """Drawable rectangle shape."""

    bbox: PictorBox
    style: PictorRectangleStyle = PictorRectangleStyle()

    def draw(self, draw: ImageDraw.Draw):
        draw.rectangle(self.bbox.raw_tuple,
                       fill=style.fill_color,
                       outline=style.outline_color,
                       width=style.outline_width)

    def copy(self) -> 'PictorRectangle':
        """Create a new instance by copying all fields."""

        return PictorRectangle(bbox=self.bbox.copy(), style=self.style.copy())
