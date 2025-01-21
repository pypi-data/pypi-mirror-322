"""Test module for the class PictorRectangle."""

from assertpy import assert_that

from src.pictor_lib.pictor_box import PictorBox
from src.pictor_lib.pictor_point import PictorPoint
from src.pictor_lib.pictor_rectangle import PictorRectangle, PictorRectangleStyle
from src.pictor_lib.pictor_size import PictorSize


# pylint: disable=too-many-public-methods
class TestPictorRectangle:
    """Tests for the class PictorRectangle."""

    def test_rectangle_style(self):
        """Test for default style."""

        rect = PictorRectangle(
            bbox=PictorBox(point=PictorPoint(67, 42), size=PictorSize(7, 5)))

        # Verify rectangle.
        assert_that(rect.style).is_equal_to(PictorRectangleStyle())

    def test_copy(self):
        """Test for the copy method."""

        old_rect = PictorRectangle(
            bbox=PictorBox(point=PictorPoint(67, 42), size=PictorSize(7, 5)))
        new_rect = old_rect.copy()

        # Verify rectangle.
        assert_that(new_rect).is_not_same_as(old_rect)
        assert_that(new_rect.bbox).is_not_same_as(old_rect.bbox)
        assert_that(new_rect.bbox.point).is_equal_to(old_rect.bbox.point)
        assert_that(new_rect.bbox.size).is_equal_to(old_rect.bbox.size)
        assert_that(new_rect.style).is_not_same_as(old_rect.style)
        assert_that(new_rect.style).is_equal_to(old_rect.style)
