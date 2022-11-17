from typing import Tuple

import pytest
from numpy import ndarray

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.Board import Board
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move


def test_should_this_piece_move_white_color_piece_should_move():
    # given
    board: Board = Board()
    expected: bool = True
    row: int = 7
    col = 0

    # when
    result = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_black_color_piece_should_not_move():
    # given
    board: Board = Board()
    expected: bool = False
    row: int = 0
    col: int = 0

    # when
    result: int = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_white_color_negative_values():
    # given
    board: Board = Board()
    row: int = -7
    col: int = -1

    # when
    with pytest.raises(IllegalArgumentException):
        result = board.should_this_piece_move(row, col)

    # then


def test_should_this_piece_move_white_color_none_values():
    # given
    board: Board = Board()
    row: int = None
    col: int = None

    # when
    with pytest.raises(NullArgumentException):
        result = board.should_this_piece_move(row, col)

    # then


def test_add_piece_to_the_board_negative_values():
    # given
    board: Board = Board()
    piece: int = -7
    square: int = -1

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_square_value_not_in_bonds():
    # given
    board: Board = Board()
    square: int = -8
    piece: int = 8

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_and_square_are_none():
    # given
    board: Board = Board()
    piece: int = None
    square: int = None

    # when
    with pytest.raises(NullArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_not_exists():
    # given
    board: Board = Board()
    square: int = 8
    piece: int = 48

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_proper_add():
    # given
    board: Board = Board()
    board_array = board.get_board_array()
    square: int = 8
    piece: int = 18
    expected: int = 18

    # when
    board.add_piece_to_the_board(piece, square)
    result: int = board_array[square]

    # then
    assert expected == result


def test_delete_piece_from_board_none_values():
    # given
    board: Board = Board()

    # when
    with pytest.raises(NullArgumentException):
        result = board.delete_piece_from_board_square(None)

    # then


def test_delete_piece_from_board_values_not_with_bonds():
    # given
    board: Board = Board()
    square: int = -86

    # when
    with pytest.raises(IllegalArgumentException):
        result = board.delete_piece_from_board_square(square)

    # then


def test_set_opposite_color_sides():
    # given
    board: Board = Board()
    expected: Tuple[int, int] = (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value)

    # when
    board.set_opposite_color_sides()
    result: Tuple[int, int] = board.get_player_color(), board.get_engine_color()

    # then
    assert expected == result


def test_castle_king_proper_use():
    # given
    board: Board = Board()
    board_array: ndarray[int] = board.get_board_array()
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected_rook_pos: int = 61
    expected_king_pos: int = 62
    rook: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    king: int = PiecesEnum.WHITE.value | PiecesEnum.KING.value

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)
    result_piece_on_rook_pos: int = board_array[expected_rook_pos]
    result_piece_on_king_pos: int = board_array[expected_king_pos]

    # then
    assert rook == result_piece_on_rook_pos and king == result_piece_on_king_pos


def test_castle_king_not_a_king():
    # given
    board: Board = Board()
    castling_move: Move = Move(60, 62, PiecesEnum.ROOK.value, -1)

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    with pytest.raises(IllegalArgumentException):
        board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)

    # then


def test_castle_king_not_castling_move():
    # given
    board: Board = Board()
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, -1)

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    with pytest.raises(IllegalArgumentException):
        board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)

    # then


def test_castle_king_null_arguments():
    # given
    board: Board = Board()

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    with pytest.raises(NullArgumentException):
        board.castle_king(None, None)

    # then


def test_un_castle_king_null_arguments():
    # given
    board: Board = Board()

    # when
    with pytest.raises(NullArgumentException):
        board.un_castle_king(None, None)

    # then


def test_un_castle_king_not_castling_move():
    # given
    board: Board = Board()
    color: int = PiecesEnum.WHITE.value
    castling_move = Move(60, 62, PiecesEnum.KING.value, -1)

    # when
    with pytest.raises(IllegalArgumentException):
        board.un_castle_king(castling_move, color)

    # then


def test_un_castle_king_not_existing_color():
    # given
    board: Board = Board()
    color: int = 81
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)

    # when
    with pytest.raises(IllegalArgumentException):
        board.un_castle_king(castling_move, color)

    # then


def test_un_castle_king_proper_use():
    # given
    board: Board = Board()
    board_array: ndarray[int] = board.get_board_array()
    castling_move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected_rook_pos: int = 63
    expected_king_pos: int = 60
    rook: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    king: int = PiecesEnum.WHITE.value | PiecesEnum.KING.value

    board.delete_piece_from_board_square(53)
    board.delete_piece_from_board_square(54)

    # when
    board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)
    board.un_castle_king(castling_move, PiecesEnum.WHITE.value)

    result_piece_on_rook_pos: int = board_array[expected_rook_pos]
    result_piece_on_king_pos: int = board_array[expected_king_pos]

    # then
    assert rook == result_piece_on_rook_pos and king == result_piece_on_king_pos
