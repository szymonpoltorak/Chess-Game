import pytest

from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.moving.generation.sliding_piece.SlidingPiecesUtil import SlidingPiecesUtil


def test_is_sliding_piece_it_is() -> None:
    # given
    piece: int = PiecesEnum.QUEEN.value
    expected: bool = True

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece(piece)

    # then
    assert expected == result


def test_is_sliding_piece_it_is_not() -> None:
    # given
    piece: int = PiecesEnum.KING.value
    expected: bool = False

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece(piece)

    # then
    assert expected == result


def test_is_sliding_piece_null_piece() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        SlidingPiecesUtil.is_it_sliding_piece(None)

    # then


def test_is_it_sliding_piece_move_bishop_not_diagonal_direction() -> None:
    # given
    piece: int = PiecesEnum.BISHOP.value
    expected: bool = False
    direction: int = MoveEnum.LEFT.value

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_bishop_diagonal_direction() -> None:
    # given
    piece: int = PiecesEnum.BISHOP.value
    expected = True
    direction: int = MoveEnum.TOP_LEFT.value

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_rook_diagonal_direction() -> None:
    # given
    piece: int = PiecesEnum.ROOK.value
    expected: bool = False
    direction: int = MoveEnum.TOP_LEFT.value

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_rook_not_diagonal_direction() -> None:
    # given
    piece: int = PiecesEnum.ROOK.value
    direction: int = MoveEnum.LEFT.value
    expected: bool = True

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_queen_not_diagonal_direction() -> None:
    # given
    piece: int = PiecesEnum.QUEEN.value
    expected: bool = True
    direction: int = MoveEnum.LEFT.value

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_queen_diagonal_direction() -> None:
    # given
    piece: int = PiecesEnum.QUEEN.value
    expected: bool = True
    direction: int = MoveEnum.TOP_LEFT.value

    # when
    result: bool = SlidingPiecesUtil.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_null_arguments() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        SlidingPiecesUtil.is_it_sliding_piece_move(None, None)

    # then


def test_is_it_sliding_piece_move_not_sliding_piece() -> None:
    # given

    # when
    with pytest.raises(IllegalArgumentException):
        SlidingPiecesUtil.is_it_sliding_piece_move(PiecesEnum.KING.value, MoveEnum.LEFT.value)

    # then


def test_is_it_sliding_piece_move_not_sliding_piece_direction() -> None:
    # given
    direction: int = 41

    # when
    with pytest.raises(IllegalArgumentException):
        SlidingPiecesUtil.is_it_sliding_piece_move(PiecesEnum.QUEEN.value, direction)

    # then
