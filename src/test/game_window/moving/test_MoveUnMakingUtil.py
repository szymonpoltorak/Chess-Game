import pytest
from numpy._typing import NDArray

from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.board.GameBoard import GameBoard
from src.main.game_window.board.fen.FenData import FenData
from src.main.game_window.board.fen.FenMaker import FenMaker
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.enums.SpecialFlags import SpecialFlags
from src.main.game_window.moving.MoveMakingUtil import MoveMakingUtil
from src.main.game_window.moving.MoveUnMakingUtil import MoveUnMakingUtil
from src.main.game_window.moving.generation.MoveGenerator import MoveGenerator
from src.main.game_window.moving.generation.data.Move import Move


def test_un_castle_king_null_arguments() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())

    # when
    with pytest.raises(NullArgumentException):
        MoveUnMakingUtil.un_castle_king(None, None, board)

    # then


def test_un_castle_king_not_castling_move() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    color: int = PiecesEnum.WHITE.value
    castling_move = Move(60, 62, PiecesEnum.KING.value, -1)

    # when
    with pytest.raises(IllegalArgumentException):
        MoveUnMakingUtil.un_castle_king(castling_move, color, board)

    # then


def test_un_castle_king_not_existing_color() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    color: int = 81
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)

    # when
    with pytest.raises(IllegalArgumentException):
        MoveUnMakingUtil.un_castle_king(castling_move, color, board)

    # then


def test_un_castle_king_proper_use() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    board_array: NDArray[int] = board.board_array()
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected_rook_pos: int = 63
    expected_king_pos: int = 60
    rook: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    king: int = PiecesEnum.WHITE.value | PiecesEnum.KING.value

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    MoveMakingUtil.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move, board)
    MoveUnMakingUtil.un_castle_king(castling_move, PiecesEnum.WHITE.value, board)

    result_piece_on_rook_pos: int = board_array[expected_rook_pos]
    result_piece_on_king_pos: int = board_array[expected_king_pos]

    # then
    assert rook == result_piece_on_rook_pos and king == result_piece_on_king_pos
