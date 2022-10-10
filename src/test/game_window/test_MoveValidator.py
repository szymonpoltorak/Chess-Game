from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move
from game_window.MoveValidator import MoveValidator


def test_is_sliding_piece_it_is():
    # given
    piece = PiecesEnum.QUEEN.value
    expected = True

    # when
    result = MoveValidator.is_sliding_piece(piece)

    # then
    assert expected == result


def test_is_sliding_piece_it_is_not():
    # given
    piece = PiecesEnum.KING.value
    expected = False

    # when
    result = MoveValidator.is_sliding_piece(piece)

    # then
    assert expected == result


def test_get_attack_direction_left_white():
    # given
    expected = -9
    direction = "LEFT"
    color = PiecesEnum.WHITE.value

    # when
    result = MoveValidator.get_attack_direction(color, direction, PiecesEnum.BLACK.value)

    # then
    assert expected == result


def test_get_attack_direction_right_black():
    # given
    expected = 9
    direction = "RIGHT"
    color = PiecesEnum.BLACK.value

    # when
    result = MoveValidator.get_attack_direction(color, direction, PiecesEnum.BLACK.value)

    # then
    assert expected == result


def test_is_pawn_promoting_white_pawn_is_promoting():
    # given
    start_square = 8
    end_square = 0
    color = PiecesEnum.WHITE.value
    move = Move(start_square, end_square, PiecesEnum.PAWN.value)
    expected = True

    # when
    result = MoveValidator.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_it_is_not_pawn():
    # given
    start_square = 8
    end_square = 0
    color = PiecesEnum.WHITE.value
    move = Move(start_square, end_square, PiecesEnum.QUEEN.value)
    expected = False

    # when
    result = MoveValidator.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_black_pawn_is_promoting():
    # given
    start_square = 56
    end_square = 63
    color = PiecesEnum.BLACK.value
    move = Move(start_square, end_square, PiecesEnum.PAWN.value)
    expected = True

    # when
    result = MoveValidator.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result
