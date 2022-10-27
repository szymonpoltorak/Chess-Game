import pytest
from numpy import array

from game_window.board.Board import Board
from game_window.board.BoardUtil import BoardUtil
from game_window.exceptions.NullArgumentException import NullArgumentException


def test_is_board_inverted_board_is_inverted():
    # given
    board = Board()
    expected = True

    # when
    board.set_opposite_color_sides()
    result = BoardUtil.is_board_inverted(board)

    # then
    assert expected == result


def test_is_board_inverted_board_is_not_inverted():
    # given
    board = Board()
    expected = False

    # when
    result = BoardUtil.is_board_inverted(board)

    # then
    assert expected == result


def test_is_board_inverted_board_is_null():
    # given
    board = None

    # when
    with pytest.raises(NullArgumentException):
        BoardUtil.is_board_inverted(board)

    # then
