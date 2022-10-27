import pytest

from game_window.board.Board import Board
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.exceptions.IllegalArgumentException import IllegalArgumentException
from game_window.exceptions.NullArgumentException import NullArgumentException
from game_window.moving.Move import Move


def test_should_this_piece_move_white_color_piece_should_move():
    # given
    board = Board()
    expected = True
    row = 7
    col = 0

    # when
    result = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_black_color_piece_should_not_move():
    # given
    board = Board()
    expected = False
    row = 0
    col = 0

    # when
    result = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_white_color_negative_values():
    # given
    board = Board()
    row = -7
    col = -1

    # when
    with pytest.raises(IllegalArgumentException):
        result = board.should_this_piece_move(row, col)

    # then


def test_should_this_piece_move_white_color_none_values():
    # given
    board = Board()
    row = None
    col = None

    # when
    with pytest.raises(NullArgumentException):
        result = board.should_this_piece_move(row, col)

    # then


def test_add_piece_to_the_board_negative_values():
    # given
    board = Board()
    piece = -7
    square = -1

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_square_value_not_in_bonds():
    # given
    board = Board()
    square = -8
    piece = 8

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_and_square_are_none():
    # given
    board = Board()
    piece = None
    square = None

    # when
    with pytest.raises(NullArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_not_exists():
    # given
    board = Board()
    square = 8
    piece = 48

    # when
    with pytest.raises(IllegalArgumentException):
        board.add_piece_to_the_board(piece, square)

    # then


def test_add_piece_to_the_board_piece_proper_add():
    # given
    board = Board()
    board_array = board.get_board_array()
    square = 8
    piece = 18
    expected = 18

    # when
    board.add_piece_to_the_board(piece, square)
    result = board_array[square]

    # then
    assert expected == result


def test_delete_piece_from_board_none_values():
    # given
    board = Board()
    row = None
    col = None

    # when
    with pytest.raises(NullArgumentException):
        result = board.delete_piece_from_board(row, col)

    # then


def test_delete_piece_from_board_values_not_with_bonds():
    # given
    board = Board()
    row = 86
    col = -7

    # when
    with pytest.raises(IllegalArgumentException):
        result = board.delete_piece_from_board(row, col)

    # then


def test_set_opposite_color_sides():
    # given
    board = Board()
    expected = (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value)

    # when
    board.set_opposite_color_sides()
    result = board.get_player_color(), board.get_engine_color()

    # then
    assert expected == result


def test_castle_king_proper_use():
    # given
    board = Board()
    board_array = board.get_board_array()
    castling_move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected_rook_pos = 61
    expected_king_pos = 62
    rook = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    king = PiecesEnum.WHITE.value | PiecesEnum.KING.value

    board.delete_piece_from_board(6, 5)
    board.delete_piece_from_board(6, 6)

    # when
    board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)
    result_piece_on_rook_pos = board_array[expected_rook_pos]
    result_piece_on_king_pos = board_array[expected_king_pos]

    # then
    assert rook == result_piece_on_rook_pos and king == result_piece_on_king_pos


def test_castle_king_not_a_king():
    # given
    board = Board()
    castling_move = Move(60, 62, PiecesEnum.ROOK.value, -1)

    board.delete_piece_from_board(6, 5)
    board.delete_piece_from_board(6, 6)

    # when
    with pytest.raises(IllegalArgumentException):
        board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)

    # then


def test_castle_king_not_castling_move():
    # given
    board = Board()
    castling_move = Move(60, 62, PiecesEnum.KING.value, -1)

    board.delete_piece_from_board(6, 5)
    board.delete_piece_from_board(6, 6)

    # when
    with pytest.raises(IllegalArgumentException):
        board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)

    # then


def test_castle_king_null_arguments():
    # given
    board = Board()

    board.delete_piece_from_board(6, 5)
    board.delete_piece_from_board(6, 6)

    # when
    with pytest.raises(NullArgumentException):
        board.castle_king(None, None)

    # then


def test_un_castle_king_null_arguments():
    # given
    board = Board()

    # when
    with pytest.raises(NullArgumentException):
        board.un_castle_king(None, None)

    # then


def test_un_castle_king_not_castling_move():
    # given
    board = Board()
    color = PiecesEnum.WHITE.value
    castling_move = Move(60, 62, PiecesEnum.KING.value, -1)

    # when
    with pytest.raises(IllegalArgumentException):
        board.un_castle_king(castling_move, color)

    # then


def test_un_castle_king_not_existing_color():
    # given
    board = Board()
    color = 81
    castling_move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)

    # when
    with pytest.raises(IllegalArgumentException):
        board.un_castle_king(castling_move, color)

    # then


def test_un_castle_king_proper_use():
    # given
    board = Board()
    board_array = board.get_board_array()
    castling_move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected_rook_pos = 63
    expected_king_pos = 60
    rook = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    king = PiecesEnum.WHITE.value | PiecesEnum.KING.value

    board.delete_piece_from_board(6, 5)
    board.delete_piece_from_board(6, 6)

    # when
    board.castle_king(PiecesEnum.WHITE.value | PiecesEnum.KING.value, castling_move)
    board.un_castle_king(castling_move, PiecesEnum.WHITE.value)

    result_piece_on_rook_pos = board_array[expected_rook_pos]
    result_piece_on_king_pos = board_array[expected_king_pos]

    # then
    assert rook == result_piece_on_rook_pos and king == result_piece_on_king_pos
