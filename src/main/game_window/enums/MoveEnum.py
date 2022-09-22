from enum import Enum


class MoveEnum(Enum):
    """
    Contains values needed for setting up movements
    """
    START_SQUARE_COLOR: str = "#c9a35e"
    END_SQUARE_COLOR: str = "#a29655"

    BOTTOM_LEFT_S: int = 7
    BOTTOM_S: int = 8
    BOTTOM_RIGHT_S: int = 9
    TOP_LEFT_S: int = -9
    TOP_RIGHT_S: int = -7
    TOP_S: int = -8
    LEFT_S: int = -1
    RIGHT_S: int = 1

    BISHOP_START_INDEX: int = 4
    PIECE_START_INDEX: int = 0
    ROOK_END_INDEX: int = 4
    PIECE_END_INDEX: int = 8

    SLIDING_DIRECTIONS_NUMBER: int = 8
    SLIDING_DIRECTIONS: tuple[int] = (TOP_LEFT_S, TOP_S, TOP_RIGHT_S, LEFT_S, RIGHT_S, BOTTOM_LEFT_S, BOTTOM_S,
                                      BOTTOM_RIGHT_S)

    KNIGHT_DIRECTIONS_NUMBER: int = 8
    KNIGHT_DIRECTIONS: tuple[int] = (-17, -15, -10, -6, 6, 10, 15, 17)
    MAX_KNIGHT_JUMP: int = 2
