import pytest

from game_window.board.fen.FenData import FenData
from game_window.enums.PiecesEnum import PiecesEnum
from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException


def test_set_castling_queen_side_to_true():
    # given
    expected: bool = True
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    color: int = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_queen_side(True, color)
    result: bool = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_set_castling_king_side_to_true():
    # given
    expected = True
    fen_data = FenData(PiecesEnum.WHITE.value)
    color: int = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_king_side(True, color)
    result: bool = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_set_castling_king_side_to_false():
    # given
    expected: bool = False
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    color: int = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_king_side(False, color)
    result: bool = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_set_castling_queen_side_to_false():
    # given
    expected: bool = False
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    color: int = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_queen_side(False, color)
    result: bool = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_can_king_castle_king_side_and_you_can():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: bool = True
    color: int = PiecesEnum.BLACK.value

    # when
    result: bool = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_can_king_castle_king_side_and_you_can_not():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: bool = False
    color: int = PiecesEnum.BLACK.value

    # when
    fen_data.set_castling_king_side(False, color)
    result: bool = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_can_king_castle_queen_side_and_you_can():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)
    expected: bool = True
    color: int = PiecesEnum.BLACK.value

    # when
    result: bool = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_can_king_castle_queen_side_and_you_can_not():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: bool = False
    color: int = PiecesEnum.BLACK.value

    # when
    fen_data.set_castling_queen_side(False, color)
    result: bool = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_update_no_sack_and_pawn_count_increment():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: int = 1

    # when
    fen_data.update_no_sack_and_pawn_count(False)
    result: int = fen_data.get_no_sack_and_pawn_count()

    # then
    assert expected == result


def test_update_no_sack_and_pawn_count_zero_counter():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)
    expected: int = 0

    # when
    fen_data.update_no_sack_and_pawn_count(True)
    result: int = fen_data.get_no_sack_and_pawn_count()

    # then
    assert expected == result


def test_can_castle_king_side_color_is_null():
    # given
    color: int = None
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.can_king_castle_king_side(color)

    # then


def test_can_castle_king_side_color_is_unknown():
    # given
    color: int = 61
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(IllegalArgumentException):
        fen_data.can_king_castle_king_side(color)

    # then


def test_can_castle_queen_side_color_is_null():
    # given
    color: int = None
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.can_king_castle_queen_side(color)

    # then


def test_can_castle_queen_side_color_is_unknown():
    # given
    color: int = 61
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(IllegalArgumentException):
        fen_data.can_king_castle_queen_side(color)

    # then


def test_set_castling_king_side_nulls():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.set_castling_king_side(None, None)

    # then


def test_set_castling_king_side_color_not_exists():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)
    color: int = 71

    # when
    with pytest.raises(IllegalArgumentException):
        fen_data.set_castling_king_side(False, color)

    # then


def test_set_castling_queen_side_nulls():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.set_castling_queen_side(None, None)

    # then


def test_set_castling_queen_side_color_not_exists():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)
    color: int = 71

    # when
    with pytest.raises(IllegalArgumentException):
        fen_data.set_castling_queen_side(False, color)

    # then


def test_update_no_sack_and_pawn_count_null_argument():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.update_no_sack_and_pawn_count(None)

    # then


def test_set_en_passant_square_nulls():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.set_en_passant_square(None)

    # then


def test_set_en_passant_square_is_not_within_bonds():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)
    square = -2

    # when
    with pytest.raises(IllegalArgumentException):
        fen_data.set_en_passant_square(square)

    # then


def test_update_fen_data_null_argument():
    # given
    fen_data = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(NullArgumentException):
        fen_data.update_fen_data(None)

    # then
