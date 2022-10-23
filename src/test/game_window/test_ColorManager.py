from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


def test_get_piece_color_piece_none_value():
    # given
    piece = PiecesEnum.NONE.value
    expected = 0

    # when
    result = ColorManager.get_piece_color(piece)

    # then
    assert expected == result


def test_get_piece_color_piece_black_color():
    # given
    piece = PiecesEnum.BLACK.value | PiecesEnum.KNIGHT.value
    expected = PiecesEnum.BLACK.value

    # when
    result = ColorManager.get_piece_color(piece)

    # then
    assert expected == result


def test_get_piece_color_piece_white_color():
    # given
    piece = PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value
    expected = PiecesEnum.WHITE.value

    # when
    result = ColorManager.get_piece_color(piece)

    # then
    assert expected == result


def test_get_opposite_piece_color_white_color():
    # given
    color = PiecesEnum.WHITE.value
    expected = PiecesEnum.BLACK.value

    # when
    result = ColorManager.get_opposite_piece_color(color)

    # then
    assert expected == result


def test_get_opposite_piece_color_black_color():
    # given
    color = PiecesEnum.BLACK.value
    expected = PiecesEnum.WHITE.value

    # when
    result = ColorManager.get_opposite_piece_color(color)

    # then
    assert expected == result


def test_pick_proper_color_even_square():
    # given
    row = 1
    col = 1
    expected = BoardEnum.PRIMARY_BOARD_COLOR.value

    # when
    result = ColorManager.pick_proper_color(row, col)

    # then
    assert expected == result


def test_pick_proper_color_odd_square():
    # given
    row = 0
    col = 1
    expected = BoardEnum.SECONDARY_BOARD_COLOR.value

    # when
    result = ColorManager.pick_proper_color(row, col)

    # then
    assert expected == result


def test_get_opposite_square_color_primary_square_color():
    # given
    color = BoardEnum.PRIMARY_BOARD_COLOR.value
    expected = BoardEnum.SECONDARY_BOARD_COLOR.value

    # when
    result = ColorManager.get_opposite_square_color(color)

    # then
    assert expected == result


def test_get_opposite_square_color_secondary_square_color():
    # given
    color = BoardEnum.SECONDARY_BOARD_COLOR.value
    expected = BoardEnum.PRIMARY_BOARD_COLOR.value

    # when
    result = ColorManager.get_opposite_square_color(color)

    # then
    assert expected == result
