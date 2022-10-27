import pytest

from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenUtil import FenUtil
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.exceptions.IllegalArgumentException import IllegalArgumentException
from game_window.exceptions.NullArgumentException import NullArgumentException


def test_convert_square_into_board_double_index_square_equals_negative_one():
    # given
    square: int = -1
    expected: str = " -"

    # when
    result: str = FenUtil.convert_square_into_board_double_index(square)

    # then
    assert expected == result


def test_convert_square_into_board_double_index_square_equals_seven():
    # given
    square: int = 7
    expected: str = " h8"

    # when
    result: str = FenUtil.convert_square_into_board_double_index(square)

    # then
    assert expected == result


def test_get_proper_letter_size_white_color():
    # given
    expected: str = "Q"
    letter: str = "q"
    color: int = PiecesEnum.WHITE.value

    # when
    result = FenUtil.get_proper_letter_size(color, letter)

    # then
    assert expected == result


def test_get_proper_letter_size_black_color():
    # given
    expected: str = "q"
    letter: str = "q"
    color: int = PiecesEnum.BLACK.value

    # when
    result = FenUtil.get_proper_letter_size(color, letter)

    # then
    assert expected == result


def test_get_color_to_move_fen_letter_white_color():
    # given
    color: int = PiecesEnum.WHITE.value
    expected: str = " w"

    # when
    result: str = FenUtil.get_color_to_move_fen_letter(color)

    # then
    assert expected == result


def test_get_color_to_move_fen_letter_black_color():
    # given
    color: int = PiecesEnum.BLACK.value
    expected: str = " b"

    # when
    result: str = FenUtil.get_color_to_move_fen_letter(color)

    # then
    assert expected == result


def test_get_proper_color_value_white_piece():
    # given
    piece: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    expected: int = PiecesEnum.WHITE.value

    # when
    result: int = FenUtil.get_proper_color_value(piece)

    # then
    assert expected == result


def test_get_proper_color_value_black_piece():
    # given
    piece: int = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    expected: int = PiecesEnum.BLACK.value

    # when
    result: int = FenUtil.get_proper_color_value(piece)

    # then
    assert expected == result


def test_get_proper_piece_for_fen_white_pawn():
    # given
    color: int = PiecesEnum.WHITE.value
    index: int = 55
    board: Board = Board()
    expected: str = "P"

    # when
    result: str = FenUtil.get_proper_piece_for_fen(board.get_board_array(), index, color)

    # then
    assert expected == result


def test_get_proper_piece_for_fen_black_rook():
    # given
    color: int = PiecesEnum.BLACK.value
    index: int = 0
    board: Board = Board()
    expected: str = "r"

    # when
    result: str = FenUtil.get_proper_piece_for_fen(board.get_board_array(), index, color)

    # then
    assert expected == result


def test_add_castling_letters_to_fen_all_castling_possible():
    # given
    board: Board = Board()
    expected: str = " KQkq"

    # when
    result: str = FenUtil.add_castling_letters_to_fen(board)

    # then
    assert expected == result


def test_add_castling_letters_to_fen_no_castling():
    # given
    board: Board = Board()
    expected: str = " -"

    # when
    board.get_fen_data().set_castling_king_side(False, PiecesEnum.WHITE.value)
    board.get_fen_data().set_castling_king_side(False, PiecesEnum.BLACK.value)
    board.get_fen_data().set_castling_queen_side(False, PiecesEnum.WHITE.value)
    board.get_fen_data().set_castling_queen_side(False, PiecesEnum.BLACK.value)

    result: str = FenUtil.add_castling_letters_to_fen(board)

    # then
    assert expected == result


def test_update_no_sack_and_pawn_counter_nulls():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.update_no_sack_and_pawn_counter(None, None, None)

    # then


def test_update_no_sack_and_pawn_counter_out_of_bonds_arguments():
    # given
    deleted_piece: int = -1
    moving_piece: int = 98
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.update_no_sack_and_pawn_counter(fen_data, deleted_piece, moving_piece)

    # then


def test_disable_castling_on_side_nulls():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.disable_castling_on_side(None, None, None)

    # then


def test_disable_castling_on_side_out_of_bonds_arguments():
    # given
    deleted_piece: int = -1
    moving_piece: int = 98
    board: Board = Board()

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.disable_castling_on_side(deleted_piece, moving_piece, board)

    # then