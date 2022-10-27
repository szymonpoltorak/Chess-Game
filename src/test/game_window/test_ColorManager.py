from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


def test_get_piece_color_piece_none_value():
    # given
    piece: int = PiecesEnum.NONE.value
    expected: int = 0

    # when
    result: int = ColorManager.get_piece_color(piece)

    # then
    assert expected == result


def test_get_piece_color_piece_black_color():
    # given
    piece: int = PiecesEnum.BLACK.value | PiecesEnum.KNIGHT.value
    expected: int = PiecesEnum.BLACK.value

    # when
    result: int = ColorManager.get_piece_color(piece)

    # then
    assert expected == result


def test_get_piece_color_piece_white_color():
    # given
    piece: int = PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value
    expected: int = PiecesEnum.WHITE.value

    # when
    result: int = ColorManager.get_piece_color(piece)

    # then
    assert expected == result


def test_get_opposite_piece_color_white_color():
    # given
    color: int = PiecesEnum.WHITE.value
    expected: int = PiecesEnum.BLACK.value

    # when
    result: int = ColorManager.get_opposite_piece_color(color)

    # then
    assert expected == result


def test_get_opposite_piece_color_black_color():
    # given
    color: int = PiecesEnum.BLACK.value
    expected: int = PiecesEnum.WHITE.value

    # when
    result: int = ColorManager.get_opposite_piece_color(color)

    # then
    assert expected == result


def test_pick_proper_color_even_square():
    # given
    row: int = 1
    col: int = 1
    expected: str = BoardEnum.PRIMARY_BOARD_COLOR.value

    # when
    result: str = ColorManager.pick_proper_color(row, col)

    # then
    assert expected == result


def test_pick_proper_color_odd_square():
    # given
    row: int = 0
    col: int = 1
    expected: str = BoardEnum.SECONDARY_BOARD_COLOR.value

    # when
    result: str = ColorManager.pick_proper_color(row, col)

    # then
    assert expected == result


def test_get_opposite_square_color_primary_square_color():
    # given
    color: str = BoardEnum.PRIMARY_BOARD_COLOR.value
    expected: str = BoardEnum.SECONDARY_BOARD_COLOR.value

    # when
    result: str = ColorManager.get_opposite_square_color(color)

    # then
    assert expected == result


def test_get_opposite_square_color_secondary_square_color():
    # given
    color: str = BoardEnum.SECONDARY_BOARD_COLOR.value
    expected: str = BoardEnum.PRIMARY_BOARD_COLOR.value

    # when
    result: str = ColorManager.get_opposite_square_color(color)

    # then
    assert expected == result
