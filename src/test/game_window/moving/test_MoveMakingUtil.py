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


def test_castle_king_proper_use() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int] = board.board_array()
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected_rook_pos: int = 61
    expected_king_pos: int = 62
    rook: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    king: int = PiecesEnum.WHITE.value | PiecesEnum.KING.value

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    MoveMakingUtil.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move, board)
    result_piece_on_rook_pos: int = board_array[expected_rook_pos]
    result_piece_on_king_pos: int = board_array[expected_king_pos]

    # then
    assert rook == result_piece_on_rook_pos and king == result_piece_on_king_pos


def test_castle_king_not_a_king() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))
    castling_move: Move = Move(60, 62, PiecesEnum.ROOK.value, -1)

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    with pytest.raises(IllegalArgumentException):
        MoveMakingUtil.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move, board)

    # then


def test_castle_king_not_castling_move() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, -1)

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    with pytest.raises(IllegalArgumentException):
        MoveMakingUtil.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move, board)

    # then


def test_castle_king_null_arguments() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)))

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    with pytest.raises(NullArgumentException):
        MoveMakingUtil.castle_king(None, None, None)

    # then
