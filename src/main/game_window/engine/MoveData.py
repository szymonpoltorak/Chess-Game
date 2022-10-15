from dataclasses import dataclass


@dataclass(slots=True)
class MoveData:
    deleted_piece: int or None
    white_castle_king: bool or None
    white_castle_queen: bool or None
    black_castle_king: bool or None
    black_castle_queen: bool or None
    en_passant_square: int or None
    en_passant_piece_square: int or None
    en_passant_piece_square: int or None
    rook_position: int or None
