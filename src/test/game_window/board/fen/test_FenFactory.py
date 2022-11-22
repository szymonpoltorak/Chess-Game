from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenFactory import FenFactory
from game_window.board.fen.FenMaker import FenMaker
from game_window.enums.PiecesEnum import PiecesEnum


def test_convert_board_array_to_fen():
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    fen_factory: FenFactory = FenMaker(FenData(PiecesEnum.WHITE.value))
    expected: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

    # when
    result: str = fen_factory.convert_board_array_to_fen(board)

    # then
    assert expected == result
