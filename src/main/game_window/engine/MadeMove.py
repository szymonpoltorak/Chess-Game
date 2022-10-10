from dataclasses import dataclass


@dataclass(slots=True)
class MadeMove:
    deleted_piece: int
    white_castle_king: bool or None
    white_castle_queen: bool or None
    black_castle_king: bool or None
    black_castle_queen: bool or None
    en_passant_square: int or None
    en_passant_piece_square: int or None
