from abc import ABC
from abc import abstractmethod
from typing import Type

from src.main.game_window.board.Board import Board


class Evaluation(ABC):
    """
    Abstract class for evaluator object classes
    """

    __slots__ = ()

    @abstractmethod
    def evaluate_position(self, board: Type[Board], favor_color: int) -> float:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: int value of favor_color in favor of which we evaluate position
        :return: float evaluation
        """
        pass
