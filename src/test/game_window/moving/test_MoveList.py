import pytest
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.moving.generation.data.Moves import Moves
from numpy import full


def test_append_null_move() -> None:
    # given
    move_list: Moves = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

    # when
    with pytest.raises(NullArgumentException):
        move_list.append(None)

    # then


def test_is_empty_list_is_empty() -> None:
    # given
    expected: bool = True
    move_list: Moves = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

    # when
    result: bool = move_list.is_empty()

    # then
    assert result == expected
