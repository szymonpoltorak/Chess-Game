import pytest

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.Board import Board
from game_window.board.BoardUtil import BoardUtil
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags


def test_is_board_inverted_board_is_inverted() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: bool = True

    # when
    board.set_opposite_color_sides()
    result: bool = BoardUtil.is_board_inverted(board)

    # then
    assert expected == result


def test_is_board_inverted_board_is_not_inverted() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: bool = False

    # when
    result: bool = BoardUtil.is_board_inverted(board)

    # then
    assert expected == result


def test_is_board_inverted_board_is_null() -> None:
    # given
    board: Board = None

    # when
    with pytest.raises(NullArgumentException):
        BoardUtil.is_board_inverted(board)

    # then


def test_get_promotion_piece_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        BoardUtil.get_promotion_piece(None, None)

    # then


def test_get_promotion_piece_illegal_color() -> None:
    # given
    color: int = -1
    flag: int = SpecialFlags.PROMOTE_TO_KNIGHT.value

    # when
    with pytest.raises(IllegalArgumentException):
        BoardUtil.get_promotion_piece(color, flag)

    # then


def test_get_promotion_piece_illegal_flag() -> None:
    # given
    color: int = PiecesEnum.WHITE.value
    flag: int = SpecialFlags.EN_PASSANT.value

    # when
    with pytest.raises(IllegalArgumentException):
        BoardUtil.get_promotion_piece(color, flag)

    # then


def test_get_promotion_piece_get_white_queen_value() -> None:
    # given
    color: int = PiecesEnum.WHITE.value
    flag: int = SpecialFlags.PROMOTE_TO_QUEEN.value
    expected: int = color | PiecesEnum.QUEEN.value

    # when
    result: int = BoardUtil.get_promotion_piece(color, flag)

    # then
    assert result == expected
