import pytest

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.Board import Board
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.PromotionData import PromotionData


def test_get_rect_index_arguments_are_nulls():
    # given
    promotion_data: PromotionData = PromotionData()

    # when
    with pytest.raises(NullArgumentException):
        promotion_data.get_rect_index(None, None)

    # then


def test_get_rect_index_arguments_are_negatives():
    # given
    promotion_data: PromotionData = PromotionData()
    rect_size: int = -1
    y: int = -2

    # when
    with pytest.raises(IllegalArgumentException):
        promotion_data.get_rect_index(y, rect_size)

    # then


def test_get_rect_index_arguments_returns_rect_index():
    # given
    promotion_data: PromotionData = PromotionData()
    promotion_data.set_promotion_data(PiecesEnum.WHITE.value, 10, 10, 31)

    rect_size: int = 20
    y: int = 40
    expected: int = 1

    # when
    result: int = promotion_data.get_rect_index(y, rect_size)

    # then
    assert result == expected


def test_get_rect_index_arguments_returns_negative_one():
    # given
    promotion_data: PromotionData = PromotionData()
    promotion_data.set_promotion_data(PiecesEnum.WHITE.value, 30, 80, 31)

    rect_size: int = 20
    y: int = 40
    expected: int = -1

    # when
    result: int = promotion_data.get_rect_index(y, rect_size)

    # then
    assert result == expected


def test_check_user_choice_null_args():
    # given
    promotion_data: PromotionData = PromotionData()

    # when
    with pytest.raises(NullArgumentException):
        promotion_data.check_user_choice(None, None, None, None)

    # then


def test_check_user_choice_arguments_are_negatives():
    # given
    promotion_data: PromotionData = PromotionData()
    rect_size: int = -1
    y: int = -2
    x: int = -3
    board: Board = Board()

    # when
    with pytest.raises(IllegalArgumentException):
        promotion_data.check_user_choice(rect_size, board, x, y)

    # then


def test_get_rect_index_null_args():
    # given
    promotion_data: PromotionData = PromotionData()

    # when
    with pytest.raises(NullArgumentException):
        promotion_data.get_rect_index(None, None)

    # then


def test_get_rect_index_illegal_args():
    # given
    promotion_data: PromotionData = PromotionData()

    # when
    with pytest.raises(IllegalArgumentException):
        promotion_data.get_rect_index(-1, -1)

    # then
