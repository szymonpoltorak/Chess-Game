import pytest
from numpy import array
from numpy import zeros

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.Move import Move


def test_find_friendly_king_squares_only_enemy_king():
    # given
    color_to_move = PiecesEnum.WHITE.value
    board_array = zeros(BoardEnum.BOARD_SIZE.value)
    board_array[30] = PiecesEnum.BLACK.value | PiecesEnum.KING.value

    # when
    with pytest.raises(ValueError):
        result = KingUtil.find_friendly_king_squares(board_array, color_to_move)

    # then


def test_find_friendly_king_squares_a_friendly_king():
    # given
    color_to_move = PiecesEnum.BLACK.value
    board_array = zeros(BoardEnum.BOARD_SIZE.value)
    index = 30
    board_array[index] = PiecesEnum.BLACK.value | PiecesEnum.KING.value
    expected = index

    # when
    result = KingUtil.find_friendly_king_squares(board_array, color_to_move)

    # then
    assert expected == result


def test_get_castling_squares_move_distance_greater_than_0():
    # given
    start_square = 4
    end_square = 6
    piece = PiecesEnum.KING.value
    move = Move(start_square, end_square, piece, SpecialFlags.CASTLING.value)
    expected = array([start_square, start_square + 1, start_square + 2])

    # when
    result = KingUtil.get_castling_squares(move)

    # then
    assert expected.all() == result.all()


def test_get_castling_squares_move_distance_less_than_0():
    # given
    start_square = 6
    end_square = 4
    piece = PiecesEnum.KING.value
    move = Move(start_square, end_square, piece, SpecialFlags.CASTLING.value)
    expected = array([start_square, start_square - 1, start_square - 2])

    # when
    result = KingUtil.get_castling_squares(move)

    # then
    assert expected.all() == result.all()
    