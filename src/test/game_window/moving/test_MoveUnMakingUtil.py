import pytest
from numpy import ndarray

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.GameBoard import GameBoard
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move
from game_window.moving.MoveMakingUtil import MoveMakingUtil
from game_window.moving.MoveUnMakingUtil import MoveUnMakingUtil


def test_un_castle_king_null_arguments() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(NullArgumentException):
        MoveUnMakingUtil.un_castle_king(None, None, board)

    # then


def test_un_castle_king_not_castling_move() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))
    color: int = PiecesEnum.WHITE.value
    castling_move = Move(60, 62, PiecesEnum.KING.value, -1)

    # when
    with pytest.raises(IllegalArgumentException):
        MoveUnMakingUtil.un_castle_king(castling_move, color, board)

    # then


def test_un_castle_king_not_existing_color() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))
    color: int = 81
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)

    # when
    with pytest.raises(IllegalArgumentException):
        MoveUnMakingUtil.un_castle_king(castling_move, color, board)

    # then


def test_un_castle_king_proper_use() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int] = board.board_array()
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
