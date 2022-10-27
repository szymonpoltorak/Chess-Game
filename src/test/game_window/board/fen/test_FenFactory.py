from game_window.board.Board import Board
from game_window.board.fen.FenFactory import FenFactory


def test_convert_board_array_to_fen():
    # given
    board = Board()
    expected = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

    # when
    result = FenFactory.convert_board_array_to_fen(board)

    # then
    assert expected == result
