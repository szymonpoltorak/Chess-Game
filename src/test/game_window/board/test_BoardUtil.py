import pytest

from game_window.board.Board import Board
from game_window.board.BoardUtil import BoardUtil
from exceptions.NullArgumentException import NullArgumentException


def test_is_board_inverted_board_is_inverted():
    # given
    board: Board = Board()
    expected: bool = True

    # when
    board.set_opposite_color_sides()
    result : bool= BoardUtil.is_board_inverted(board)

    # then
    assert expected == result


def test_is_board_inverted_board_is_not_inverted():
    # given
    board: Board = Board()
    expected: bool = False

    # when
    result: bool = BoardUtil.is_board_inverted(board)

    # then
    assert expected == result


def test_is_board_inverted_board_is_null():
    # given
    board: Board = None

    # when
    with pytest.raises(NullArgumentException):
        BoardUtil.is_board_inverted(board)

    # then
