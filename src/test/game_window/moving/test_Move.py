from game_window.enums.MoveEnum import MoveEnum
from game_window.moving.Move import Move


def test_set_start_square_none_values():
    # given
    move: Move = Move(0, 1, 2, -1)
    expected: int = -1

    # when
    move.set_start_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
    result: int = move.get_start_square()

    # then
    assert expected == result


def test_end_start_square_none_values():
    # given
    move: Move = Move(0, 1, 2, -1)
    expected: int = -1

    # when
    move.set_end_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
    result: int = move.get_end_square()

    # then
    assert expected == result
