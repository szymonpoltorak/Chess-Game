from game_window.board.Board import Board
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveMaker import MoveMaker


def test_make_move():
    # given
    board: Board = Board()
    expected: int = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    color: int = PiecesEnum.WHITE.value
    start_square: int = 63
    end_square: int = 0
    move: Move = Move(start_square, end_square, PiecesEnum.ROOK.value, SpecialFlags.NONE.value)

    # when
    result: MoveData = MoveMaker.make_move(move, color, board)

    # then
    assert expected == result.deleted_piece


def test_un_make_move():
    # given
    board = Board()
    expected: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_piece: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_data: MoveData = MoveData(deleted_piece, None, None, None, None, None, None)
    start_square: int = 63
    end_square: int = 0
    move: Move = Move(start_square, end_square, PiecesEnum.ROOK.value, SpecialFlags.NONE.value)

    # when
    MoveMaker.un_make_move(move, deleted_data, board)
    result: int = board.get_board_array()[end_square]

    # then
    assert expected == result
