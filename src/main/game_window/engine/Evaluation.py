from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_window.board.Board import Board


class Evaluation(ABC):
    """
    Abstract class for evaluator object classes
    """

    @abstractmethod
    def evaluate_position(self, board: 'Board', favor_color: int) -> float:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: int value of favor_color in favor of which we evaluate position
        :return: float evaluation
        """
        pass
