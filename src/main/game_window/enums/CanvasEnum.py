from enum import Enum


class CanvasEnum(Enum):
    """
    PyGame surface settings values.
    """

    __slots__ = ()

    CANVAS_WIDTH: int = 696
    CANVAS_HEIGHT: int = 696

    CANVAS_X: int = 150
    CANVAS_Y: int = 55

    FIRST_COLUMN: int = 0
    LAST_ROW: int = 7
