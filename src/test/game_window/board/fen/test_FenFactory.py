from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenFactory import FenFactory
from game_window.board.fen.FenMaker import FenMaker
from game_window.board.GameBoard import GameBoard
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.MoveGenerator import MoveGenerator


def test_convert_board_array_to_fen() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    fen_factory: FenFactory = FenMaker(FenData(PiecesEnum.WHITE.value))
    expected: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"

    # when
    result: str = fen_factory.convert_board_array_to_fen(board)

    # then
    assert expected == result
