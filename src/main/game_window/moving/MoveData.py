from dataclasses import dataclass


@dataclass(slots=True, order=True, unsafe_hash=True, eq=True)
class MoveData:
    """
    Class containing data for making and unmaking moves
    """
    deleted_piece: int
    white_castle_king: bool
    white_castle_queen: bool
    black_castle_king: bool
    black_castle_queen: bool
    en_passant_square: int
    en_passant_piece_square: int
