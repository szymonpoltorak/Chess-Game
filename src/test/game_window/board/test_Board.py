from typing import Tuple

import pytest

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.enums.PiecesEnum import PiecesEnum


def test_should_this_piece_move_white_color_piece_should_move():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: bool = True
    row: int = 7
    col = 0

    # when
    result = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_black_color_piece_should_not_move():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: bool = False
    row: int = 0
    col: int = 0

    # when
    result: int = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_white_color_negative_values():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    row: int = -7
    col: int = -1

    # when
    with pytest.raises(IllegalArgumentException):
        result = board.should_this_piece_move(row, col)

    # then


def test_should_this_piece_move_white_color_none_values():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    row: int = None
    col: int = None

    # when
    with pytest.raises(NullArgumentException):
        result = board.should_this_piece_move(row, col)

    # then


def test_add_piece_to_the_board_negative_values():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    piece: int = -7
    square: int = -1

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_square_value_not_in_bonds():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    square: int = -8
    piece: int = 8

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_and_square_are_none():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    piece: int = None
    square: int = None

    # when
    with pytest.raises(NullArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_not_exists():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    square: int = 8
    piece: int = 48

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_proper_add():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array = board.board_array()
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
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(NullArgumentException):
        result = board.delete_piece_from_board_square(None)

    # then


def test_delete_piece_from_board_values_not_with_bonds():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    square: int = -86

    # when
    with pytest.raises(IllegalArgumentException):
        result = board.delete_piece_from_board_square(square)

    # then


def test_set_opposite_color_sides():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: Tuple[int, int] = (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value)

    # when
    board.set_opposite_color_sides()
    result: Tuple[int, int] = board.player_color(), board.engine_color()

    # then
    assert expected == result
