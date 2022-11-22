import pytest

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.board.fen.FenUtil import FenUtil
from game_window.ColorManager import ColorManager
from game_window.enums.PiecesEnum import PiecesEnum


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


def test_get_proper_piece_for_fen_white_pawn():
    # given
    color: int = PiecesEnum.WHITE.value
    index: int = 55
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: str = "P"

    # when
    result: str = FenUtil.get_proper_piece_for_fen(board.board_array(), index, color)

    # then
    assert expected == result


def test_get_proper_piece_for_fen_black_rook():
    # given
    color: int = PiecesEnum.BLACK.value
    index: int = 0
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: str = "r"

    # when
    result: str = FenUtil.get_proper_piece_for_fen(board.board_array(), index, color)

    # then
    assert expected == result


def test_add_castling_letters_to_fen_all_castling_possible():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: str = " KQkq"

    # when
    result: str = FenUtil.get_castling_letters_to_fen(fen_data)

    # then
    assert expected == result


def test_add_castling_letters_to_fen_no_castling():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: str = " -"

    # when
    fen_data.set_castling_king_side(False, PiecesEnum.WHITE.value)
    fen_data.set_castling_king_side(False, PiecesEnum.BLACK.value)
    fen_data.set_castling_queen_side(False, PiecesEnum.WHITE.value)
    fen_data.set_castling_queen_side(False, PiecesEnum.BLACK.value)

    result: str = FenUtil.get_castling_letters_to_fen(fen_data)

    # then
    assert expected == result


def test_update_no_sack_and_pawn_counter_nulls():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(NullArgumentException):
        board.update_no_sack_and_pawn_counter(None, None)

    # then


def test_update_no_sack_and_pawn_counter_out_of_bonds_arguments():
    # given
    deleted_piece: int = -1
    moving_piece: int = 98
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(IllegalArgumentException):
        board.update_no_sack_and_pawn_counter(deleted_piece, moving_piece)

    # then


def test_disable_castling_on_side_nulls():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(NullArgumentException):
        board.disable_castling_on_side(None, None)

    # then


def test_disable_castling_on_side_out_of_bonds_arguments():
    # given
    color: int = -1
    target_square: int = 98
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(IllegalArgumentException):
        board.disable_castling_on_side(color, target_square)

    # then


def test_disable_castling_if_deleted_rook_nulls_arguments():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(NullArgumentException):
        board.disable_castling_if_captured_rook(None, None, None)

    # then


def test_disable_castling_if_deleted_rook_arguments_not_within_bonds():
    # given
    deleted_piece: int = 13
    color: int = 90
    square: int = -1
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))

    # when
    with pytest.raises(IllegalArgumentException):
        board.disable_castling_if_captured_rook(deleted_piece, color, square)

    # then


def test_disable_castling_if_deleted_rook_proper_use():
    # given
    color: int = PiecesEnum.WHITE.value
    deleted_piece: int = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    square: int = 7
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: bool = False

    # when
    board.disable_castling_if_captured_rook(deleted_piece, color, square)
    result: bool = board.can_king_castle_king_side(ColorManager.get_opposite_piece_color(color))

    # then
    assert result == expected


def test_convert_square_into_board_double_index_null_square():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.convert_square_into_board_double_index(None)

    # then


def test_get_castling_letters_to_fen_null():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.get_castling_letters_to_fen(None)

    # then


def test_get_proper_piece_for_fen_null():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.get_proper_piece_for_fen(None, None, None)

    # then


def test_get_proper_piece_for_fen_illegal_args():
    # given

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.get_proper_piece_for_fen(Board(FenMaker(FenData(PiecesEnum.WHITE.value))).board_array(), -1, 8)

    # then


def test_get_castling_letters_to_unable_castlings():
    # given
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: str = " -"

    fen_data.set_castling_king_side(False, PiecesEnum.WHITE.value)
    fen_data.set_castling_king_side(False, PiecesEnum.BLACK.value)
    fen_data.set_castling_queen_side(False, PiecesEnum.WHITE.value)
    fen_data.set_castling_queen_side(False, PiecesEnum.BLACK.value)

    # when
    result: str = FenUtil.get_castling_letters_to_fen(fen_data)

    # then
    assert result == expected


def test_convert_square_into_board_double_index_illegal_arguments():
    # given
    square: int = -9

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.convert_square_into_board_double_index(square)

    # then


def test_convert_square_into_board_double_index_square_is_negative_one():
    # given
    square: int = -1
    expected: str = " -"

    # when
    result: str = FenUtil.convert_square_into_board_double_index(square)

    # then
    assert result == expected


def test_convert_square_into_board_double_index_square_equal_to_zero():
    # given
    square: int = 0
    expected: str = " a8"

    # when
    result: str = FenUtil.convert_square_into_board_double_index(square)

    # then
    assert result == expected


def test_get_color_to_move_fen_letter_null_argument():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.get_color_to_move_fen_letter(None)

    # then


def test_get_color_to_move_fen_letter_illegal_argument():
    # given
    color: int = -9

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.get_color_to_move_fen_letter(color)

    # then


def test_get_color_to_move_fen_letter_proper_use():
    # given
    color: int = PiecesEnum.WHITE.value
    expected: str = " w"

    # when
    result: str = FenUtil.get_color_to_move_fen_letter(color)

    # then
    assert result == expected


def test_get_proper_letter_size_null_argument():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.get_proper_letter_size(None, None)

    # then


def test_get_proper_letter_size_illegal_argument():
    # given
    color: int = -9
    letter: str = "w"

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.get_proper_letter_size(color, letter)

    # then


def test_get_proper_letter_size_proper_use():
    # given
    color: int = PiecesEnum.WHITE.value
    letter: str = "w"
    expected: str = "W"

    # when
    result: str = FenUtil.get_proper_letter_size(color, letter)

    # then
    assert result == expected


def test_add_castling_letters_to_fen_null_argument():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.get_castling_letters_to_fen(None)

    # then


def test_get_proper_piece_for_fen_nulls():
    # given

    # when
    with pytest.raises(NullArgumentException):
        FenUtil.get_proper_piece_for_fen(None, None, None)

    # then


def test_get_proper_piece_for_fen_illegal_args():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    index: int = -1
    color: int = PiecesEnum.WHITE.value

    # when
    with pytest.raises(IllegalArgumentException):
        FenUtil.get_proper_piece_for_fen(board.board_array(), index, color)

    # then
