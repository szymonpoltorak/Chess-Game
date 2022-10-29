from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, order=True, unsafe_hash=True, eq=True)
class MoveData:
    """
    Class containing data for making and unmaking moves
    """
    deleted_piece: Optional[int]
    white_castle_king: Optional[bool]
    white_castle_queen: Optional[bool]
    black_castle_king: Optional[bool]
    black_castle_queen: Optional[bool]
    en_passant_square: Optional[int]
    en_passant_piece_square: Optional[int]
