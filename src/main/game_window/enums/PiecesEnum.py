from enum import Enum


class PiecesEnum(Enum):
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
    SCALE_X: int = 4
    SCALE_Y: int = 4
