from abc import ABC
from abc import abstractmethod

from game_window.board.Board import Board
from game_window.Canvas import Canvas
from game_window.engine.Engine import Engine
from game_window.moving.generation.data.Move import Move
from game_window.Promoter import Promoter


class GameWindowFactory(ABC):
    """
    Abstract class for initializer of GameWindow
    """

    __slots__ = ()

    @abstractmethod
    def create_board(self) -> Board:
        """
        Method used to init Board
        :return: Board instance
        """
        pass

    @abstractmethod
    def create_engine(self) -> Engine:
        """
        Method used to init Engine
        :return: Engine instance
        """
        pass

    @abstractmethod
    def create_promoter(self) -> Promoter:
        """
        Method used to init Promoter
        :return: Promoter instance
        """
        pass

    @abstractmethod
    def create_game_canvas(self) -> Canvas:
        """
        Method used to init Canvas
        :return: Canvas instance
        """
        pass

    @abstractmethod
    def create_non_move(self) -> Move:
        """
        Method used to init none Move
        :return: Move instance
        """
        pass
