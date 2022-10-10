from enum import Enum


class EvalEnum(Enum):
    QUEEN: int = 90
    BISHOP: int = 30
    KNIGHT: int = 30
    PAWN: int = 13
    ROOK: int = 50
    KING: int = 25
    CENTER: int = 8
    WALKED: int = 10
