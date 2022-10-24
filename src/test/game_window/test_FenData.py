from game_window.board.fen.FenData import FenData
from game_window.enums.PiecesEnum import PiecesEnum


def test_set_castling_queen_side_to_true():
    # given
    expected = True
    fen_data = FenData()
    color = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_queen_side(True, color)
    result = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_set_castling_king_side_to_true():
    # given
    expected = True
    fen_data = FenData()
    color = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_king_side(True, color)
    result = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_set_castling_king_side_to_false():
    # given
    expected = False
    fen_data = FenData()
    color = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_king_side(False, color)
    result = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_set_castling_queen_side_to_false():
    # given
    expected = False
    fen_data = FenData()
    color = PiecesEnum.WHITE.value

    # when
    fen_data.set_castling_queen_side(False, color)
    result = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_can_king_castle_king_side_and_you_can():
    # given
    fen_data = FenData()
    expected = True
    color = PiecesEnum.BLACK.value

    # when
    result = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_can_king_castle_king_side_and_you_can_not():
    # given
    fen_data = FenData()
    expected = False
    color = PiecesEnum.BLACK.value

    # when
    fen_data.set_castling_king_side(False, color)
    result = fen_data.can_king_castle_king_side(color)

    # then
    assert expected == result


def test_can_king_castle_queen_side_and_you_can():
    # given
    fen_data = FenData()
    expected = True
    color = PiecesEnum.BLACK.value

    # when
    result = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_can_king_castle_queen_side_and_you_can_not():
    # given
    fen_data = FenData()
    expected = False
    color = PiecesEnum.BLACK.value

    # when
    fen_data.set_castling_queen_side(False, color)
    result = fen_data.can_king_castle_queen_side(color)

    # then
    assert expected == result


def test_update_no_sack_and_pawn_count_increment():
    # given
    fen_data = FenData()
    expected = 1

    # when
    fen_data.update_no_sack_and_pawn_count(False)
    result = fen_data.get_no_sack_and_pawn_count()

    # then
    assert expected == result


def test_update_no_sack_and_pawn_count_zero_counter():
    # given
    fen_data = FenData()
    expected = 0

    # when
    fen_data.update_no_sack_and_pawn_count(True)
    result = fen_data.get_no_sack_and_pawn_count()

    # then
    assert expected == result
