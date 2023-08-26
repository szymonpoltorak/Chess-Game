from src.main.game_window.Canvas import Canvas
from src.main.game_window.Promoter import Promoter
from src.main.game_window.PromotionData import PromotionData
from src.main.game_window.board.Board import Board
from src.main.game_window.board.GameBoard import GameBoard
from src.main.game_window.board.fen.FenData import FenData
from src.main.game_window.board.fen.FenFactory import FenFactory
from src.main.game_window.board.fen.FenMaker import FenMaker
from src.main.game_window.engine.Engine import Engine
from src.main.game_window.engine.EnginePlayer import EnginePlayer
from src.main.game_window.engine.Evaluation import Evaluation
from src.main.game_window.engine.Evaluator import Evaluator
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.init_factory.GameWindowFactory import GameWindowFactory
from src.main.game_window.moving.generation.Generator import Generator
from src.main.game_window.moving.generation.MoveGenerator import MoveGenerator
from src.main.game_window.moving.generation.data.Move import Move


class GameWindowInit(GameWindowFactory):
    """
    Implementation of GameWindowFactory abstract class
    """

    __slots__ = ()

    def create_board(self) -> Board:
        """
        Method used to init Board
        :return: Board instance
        """
        fen_factory: FenFactory = FenMaker(FenData(PiecesEnum.WHITE.value))
        generator: Generator = MoveGenerator()

        return GameBoard(fen_factory, generator)

    def create_engine(self) -> Engine:
        """
        Method used to init Engine
        :return: Engine instance
        """
        generator: Generator = MoveGenerator()
        evaluator: Evaluation = Evaluator()

        return EnginePlayer(generator, evaluator)

    def create_promoter(self) -> Promoter:
        """
        Method used to init Promoter
        :return: Promoter instance
        """
        return PromotionData()

    def create_game_canvas(self) -> Canvas:
        """
        Method used to init Canvas
        :return: Canvas instance
        """
        return Canvas()

    def create_non_move(self) -> Move:
        """
        Method used to init none Move
        :return: Move instance
        """
        return Move(MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value)
