from enum import Enum


class MoveEnum(Enum):
    START_SQUARE_COLOR: str = "#c9a35e"
    END_SQUARE_COLOR: str = "#a29655"

    BOTTOM_LEFT: int = 7
    BOTTOM: int = 8
    BOTTOM_RIGHT: int = 9
    TOP_LEFT: int = -9
    TOP_RIGHT: int = -7
    TOP: int = -8
    LEFT: int = -1
    RIGHT: int = 1

    BISHOP_START_INDEX: int = 4
    PIECE_START_INDEX: int = 0
    ROOK_END_INDEX: int = 4
    PIECE_END_INDEX: int = 8

    DIRECTIONS: tuple[int] = (BOTTOM, TOP, LEFT, RIGHT, BOTTOM_LEFT, TOP_LEFT, BOTTOM_RIGHT, TOP_RIGHT)
