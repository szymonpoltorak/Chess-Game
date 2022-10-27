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
    MAIN_CENTER: int = 4
    SIDE_CENTER: int = 2
    WALKED: int = 3

    BISHOP_PAIR: int = 10
    FREE_LINE: int = 10
