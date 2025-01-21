"""Module that defines the PictorPoint class."""
from decimal import Decimal

from dataclasses import dataclass
from src.pictor_lib.pictor_type import DecimalUnion


@dataclass(frozen=True)
class PictorPoint:
    """Immutable data class wrapping 2d point (x, y)."""

    x: Decimal = 0
    y: Decimal = 0

    def __post_init__(self):
        object.__setattr__(self, 'x', self._convert(self.x))
        object.__setattr__(self, 'y', self._convert(self.y))

    @property
    def raw_tuple(self) -> tuple[int, int]:
        """Convert to rounded int tuple which can be used in raw Pillow APIs."""

        return round(self.x), round(self.y)

    def copy(self) -> 'PictorPoint':
        """Create a new instance by copying all fields."""

        return PictorPoint(x=self.x, y=self.y)

    def move(self, dx: DecimalUnion, dy: DecimalUnion) -> 'PictorPoint':
        """Create a new instance by moving by given (dx, dy) offset."""

        return PictorPoint(x=self.x + dx, y=self.y + dy)

    @staticmethod
    def _convert(value: DecimalUnion) -> Decimal:
        return Decimal(value)

    @staticmethod
    def from_tuple(xy: tuple[DecimalUnion, DecimalUnion]) -> 'PictorPoint':
        """Create a new instance from tuple."""

        return PictorPoint(x=PictorPoint._convert(xy[0]),
                           y=PictorPoint._convert(xy[1]))


PictorPoint.ORIGIN = PictorPoint(x=0, y=0)
