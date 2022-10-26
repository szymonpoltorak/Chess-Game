from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.pawns.PawnUtil import PawnUtil
from game_window.moving.Move import Move


def test_get_attack_direction_left_white():
    # given
    expected = -9
    direction = "LEFT"
    color = PiecesEnum.WHITE.value

    # when
    result = PawnUtil.get_attack_direction(color, direction, PiecesEnum.BLACK.value)

    # then
    assert expected == result


def test_get_attack_direction_right_black():
    # given
    expected = 9
    direction = "RIGHT"
    color = PiecesEnum.BLACK.value

    # when
    result = PawnUtil.get_attack_direction(color, direction, PiecesEnum.BLACK.value)

    # then
    assert expected == result


def test_is_pawn_promoting_white_pawn_is_promoting():
    # given
    start_square = 8
    end_square = 0
    color = PiecesEnum.WHITE.value
    move = Move(start_square, end_square, PiecesEnum.PAWN.value, SpecialFlags.PROMOTE_TO_ROOK.value)
    expected = True

    # when
    result = PawnUtil.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_it_is_not_pawn():
    # given
    start_square = 8
    end_square = 0
    color = PiecesEnum.WHITE.value
    move = Move(start_square, end_square, PiecesEnum.QUEEN.value, SpecialFlags.NONE.value)
    expected = False

    # when
    result = PawnUtil.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_black_pawn_is_promoting():
    # given
    start_square = 56
    end_square = 63
    color = PiecesEnum.BLACK.value
    move = Move(start_square, end_square, PiecesEnum.PAWN.value, SpecialFlags.PROMOTE_TO_QUEEN.value)
    expected = True

    # when
    result = PawnUtil.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result
    