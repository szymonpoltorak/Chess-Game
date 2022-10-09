from game_window.Board import Board
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move
from game_window.MoveUtil import MoveUtil


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


def test_make_move():
    # given
    board = Board()
    expected = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    color = PiecesEnum.WHITE.value
    start_square = 63
    end_square = 0
    move = Move(start_square, end_square, PiecesEnum.ROOK.value)

    # when
    result = MoveUtil.make_move(move, color, board.get_board_array())

    # then
    assert expected == result


def test_un_make_move():
    # given
    board = Board()
    expected = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_piece = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    start_square = 63
    end_square = 0
    move = Move(start_square, end_square, PiecesEnum.ROOK.value)

    # when
    MoveUtil.un_make_move(move, deleted_piece, board.get_board_array())
    result = board.get_board_array()[end_square]

    # then
    assert expected == result
