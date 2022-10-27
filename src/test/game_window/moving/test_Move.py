from game_window.moving.Move import Move


def test_set_start_square_none_values():
    # given
    move: Move = Move(0, 1, 2, -1)
    expected: bool = None

    # when
    move.set_start_square(None, None)
    result: bool = move.get_start_square()

    # then
    assert expected == result


def test_end_start_square_none_values():
    # given
    move: Move = Move(0, 1, 2, -1)
    expected: bool = None

    # when
    move.set_end_square(None, None)
    result: bool = move.get_end_square()

    # then
    assert expected == result
