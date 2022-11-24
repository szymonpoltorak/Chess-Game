from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_window.board.Board import Board


class StaticEvaluation(ABC):
    """
    Abstract class for static evaluator
    """

    @abstractmethod
    def evaluate_static_position(self, board: 'Board', favor_color: int) -> float:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: float value of color in favor of which we evaluate position
        :return: float evaluation
        """
        pass
