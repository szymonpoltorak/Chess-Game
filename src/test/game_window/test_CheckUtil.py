from numpy import array
from numpy import zeros

from game_window.CheckUtil import CheckUtil
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move


def test_find_friendly_king_squares_only_enemy_king():
    # given
    color_to_move = PiecesEnum.WHITE.value
    board_array = zeros(BoardEnum.BOARD_SIZE.value)
    board_array[30] = PiecesEnum.BLACK.value | PiecesEnum.KING.value
    expected = -1

    # when
    result = CheckUtil.find_friendly_king_squares(board_array, color_to_move)

    # then
    assert expected == result


def test_find_friendly_king_squares_a_friendly_king():
    # given
    color_to_move = PiecesEnum.BLACK.value
    board_array = zeros(BoardEnum.BOARD_SIZE.value)
    index = 30
    board_array[index] = PiecesEnum.BLACK.value | PiecesEnum.KING.value
    expected = index

    # when
    result = CheckUtil.find_friendly_king_squares(board_array, color_to_move)

    # then
    assert expected == result


def test_get_castling_squares_move_distance_greater_than_0():
    # given
    start_square = 4
    end_square = 6
    piece = PiecesEnum.KING.value
    move = Move(start_square, end_square, piece)
    expected = array([start_square, start_square + 1, start_square + 2])

    # when
    result = CheckUtil.get_castling_squares(move)

    # then
    assert expected.all() == result.all()


def test_get_castling_squares_move_distance_less_than_0():
    # given
    start_square = 6
    end_square = 4
    piece = PiecesEnum.KING.value
    move = Move(start_square, end_square, piece)
    expected = array([start_square, start_square - 1, start_square - 2])

    # when
    result = CheckUtil.get_castling_squares(move)

    # then
    assert expected.all() == result.all()
