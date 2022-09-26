from enum import Enum


class SpecialFlags(Enum):
    EN_PASSANT: int = 1
    CASTLING: int = 2
    PROMOTE_TO_QUEEN: int = 3
    PROMOTE_TO_KNIGHT: int = 4
    PROMOTE_TO_ROOK: int = 5
    PROMOTE_TO_BISHOP: int = 6