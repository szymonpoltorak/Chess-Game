from enum import Enum


class EvalEnum(Enum):
    """
    Enum containing evaluation values for certain things
    """
    QUEEN: int = 70
    BISHOP: int = 30
    KNIGHT: int = 25
    PAWN: int = 10
    ROOK: int = 40
    KING: int = 15
    MAIN_CENTER: int = 6
    SIDE_CENTER: int = 3
    WALKED: int = 3

    BISHOP_PAIR: float = 10
    FREE_LINE: float = 10
