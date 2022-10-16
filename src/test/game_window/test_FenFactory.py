from game_window.Board import Board
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.FenFactory import FenFactory


def test_get_proper_letter_size_white_color():
    # given
    expected = "Q"
    letter = "q"
    color = PiecesEnum.WHITE.value

    # when
    result = FenFactory.get_proper_letter_size(color, letter)

    # then
    assert expected == result


def test_get_proper_letter_size_black_color():
    # given
    expected = "q"
    letter = "q"
    color = PiecesEnum.BLACK.value

    # when
    result = FenFactory.get_proper_letter_size(color, letter)

    # then
    assert expected == result


def test_get_color_to_move_fen_letter_white_color():
    # given
    color = PiecesEnum.WHITE.value
    expected = " w"

    # when
    result = FenFactory.get_color_to_move_fen_letter(color)

    # then
    assert expected == result


def test_get_color_to_move_fen_letter_black_color():
    # given
    color = PiecesEnum.BLACK.value
    expected = " b"

    # when
    result = FenFactory.get_color_to_move_fen_letter(color)

    # then
    assert expected == result


def test_get_proper_color_value_white_piece():
    # given
    piece = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    expected = PiecesEnum.WHITE.value

    # when
    result = FenFactory.get_proper_color_value(piece)

    # then
    assert expected == result


def test_get_proper_color_value_black_piece():
    # given
    piece = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    expected = PiecesEnum.BLACK.value

    # when
    result = FenFactory.get_proper_color_value(piece)

    # then
    assert expected == result


def test_get_proper_piece_for_fen_white_pawn():
    # given
    color = PiecesEnum.WHITE.value
    index = 55
    board = Board()
    expected = "P"

    # when
    result = FenFactory.get_proper_piece_for_fen(board.get_board_array(), index, color)

    # then
    assert expected == result


def test_get_proper_piece_for_fen_black_rook():
    # given
    color = PiecesEnum.BLACK.value
    index = 0
    board = Board()
    expected = "r"

    # when
    result = FenFactory.get_proper_piece_for_fen(board.get_board_array(), index, color)

    # then
    assert expected == result


def test_add_castling_letters_to_fen_all_castling_possible():
    # given
    board = Board()
    expected = " KQkq"

    # when
    result = FenFactory.add_castling_letters_to_fen(board)

    # then
    assert expected == result


def test_add_castling_letters_to_fen_no_castling():
    # given
    board = Board()
    expected = " -"

    # when
    board.get_fen_data().set_castling_king_side(False, PiecesEnum.WHITE.value)
    board.get_fen_data().set_castling_king_side(False, PiecesEnum.BLACK.value)
    board.get_fen_data().set_castling_queen_side(False, PiecesEnum.WHITE.value)
    board.get_fen_data().set_castling_queen_side(False, PiecesEnum.BLACK.value)

    result = FenFactory.add_castling_letters_to_fen(board)

    # then
    assert expected == result


def test_convert_board_array_to_fen():
    # given
    board = Board()
    expected = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

    # when
    result = FenFactory.convert_board_array_to_fen(board)

    # then
    assert expected == result


def test_convert_square_into_board_double_index_square_equals_negative_one():
    # given
    square = -1
    expected = " -"

    # when
    result = FenFactory.convert_square_into_board_double_index(square)

    # then
    assert expected == result


def test_convert_square_into_board_double_index_square_equals_seven():
    # given
    square = 7
    expected = " h8"

    # when
    result = FenFactory.convert_square_into_board_double_index(square)

    # then
    assert expected == result
