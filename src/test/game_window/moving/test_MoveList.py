import pytest
from numpy import full

from exceptions.NullArgumentException import NullArgumentException
from game_window.enums.MoveEnum import MoveEnum
from game_window.moving.MoveList import MoveList


def test_append_null_move():
    # given
    move_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

    # when
    with pytest.raises(NullArgumentException):
        move_list.append(None)

    # then


def test_is_empty_list_is_empty():
    # given
    expected: bool = True
    move_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

    # when
    result: bool = move_list.is_empty()

    # then
    assert result == expected