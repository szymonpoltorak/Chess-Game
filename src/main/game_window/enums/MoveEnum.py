from enum import Enum

from typing import Tuple


class MoveEnum(Enum):
    """
    Contains values needed for setting up movements
    """

    __slots__ = ()

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

    SLIDING_DIRECTIONS_NUMBER: int = 8
    SLIDING_DIRECTIONS: Tuple[int, ...] = (TOP_LEFT, TOP, TOP_RIGHT, LEFT, RIGHT, BOTTOM_LEFT, BOTTOM, BOTTOM_RIGHT)

    KNIGHT_DIRECTIONS: Tuple[int, ...] = (-17, -15, -10, -6, 6, 10, 15, 17)
    MAX_KNIGHT_JUMP: int = 2

    ROOK_DIRECTIONS: Tuple[int, ...] = (TOP, LEFT, RIGHT, BOTTOM)
    ROOK_DIRECTIONS_INDEXES: Tuple[int, ...] = (1, 3, 4, 6)

    KK_DIRECTIONS_NUMBER: int = 8

    KING_RANGE: int = 1
    KING_DIRECTIONS: Tuple[int, ...] = (TOP_LEFT, TOP, TOP_RIGHT, LEFT, RIGHT, BOTTOM_LEFT, BOTTOM, BOTTOM_RIGHT)
    CASTLE_MOVE: int = 2
    KING_SIDE: int = 2
    QUEEN_SIDE: int = 3

    BOTTOM_ROOK_QUEEN: int = 56
    BOTTOM_ROOK_KING: int = 63
    TOP_ROOK_QUEEN: int = 0
    TOP_ROOK_KING: int = 7

    PAWN_RANGE: int = 1
    PAWN_UP_SINGLE_MOVE: int = -8
    PAWN_UP_DOUBLE_MOVE: int = -16
    PAWN_UP_LEFT_ATTACK: int = -9
    PAWN_UP_RIGHT_ATTACK: int = -7

    PAWN_DOWN_SINGLE_MOVE: int = 8
    PAWN_DOWN_DOUBLE_MOVE: int = 16
    PAWN_DOWN_LEFT_ATTACK: int = 7
    PAWN_DOWN_RIGHT_ATTACK: int = 9

    EN_PASSANT_PIECE_SQUARES: Tuple[int, ...] = (24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39)
    ENGINE_EN_PASSANT_SQUARES: Tuple[int, ...] = (40, 41, 42, 43, 44, 45, 46, 47)
    PLAYER_EN_PASSANT_SQUARES: Tuple[int, ...] = (16, 17, 18, 19, 20, 21, 22, 23)

    NONE_EN_PASSANT_SQUARE: int = -1
    MAX_NUM_OF_MOVES: int = 80

    TOP_DIR: int = 1
    TOP_STEP: int = -8
    LEFT_DIR: int = 3
    LEFT_STEP: int = -1

    NONE: int = -1
