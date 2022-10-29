from enum import Enum
from typing import Tuple


class PiecesEnum(Enum):
    """
    Enum consists of values important for pieces on chess board.
    """
    NONE: int = 0
    KING: int = 1
    PAWN: int = 2
    KNIGHT: int = 3
    BISHOP: int = 4
    ROOK: int = 5
    QUEEN: int = 6

    WHITE: int = 8
    BLACK: int = 16

    SCALE_WIDTH: int = 75
    SCALE_HEIGHT: int = 75
    SCALE_X: int = 5
    SCALE_Y: int = 5

    PIECES_TUPLE: Tuple[int, ...] = (0, 1, 2, 3, 4, 5, 6)
