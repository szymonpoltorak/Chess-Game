from enum import Enum


class EvalEnum(Enum):
    QUEEN: int = 70
    BISHOP: int = 30
    KNIGHT: int = 25
    PAWN: int = 10
    ROOK: int = 40
    KING: int = 15
    CENTER: int = 4
    WALKED: int = 3
