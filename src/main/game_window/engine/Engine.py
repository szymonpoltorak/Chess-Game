from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from game_window.moving.generation.data.Move import Move

if TYPE_CHECKING:
    from game_window.board.Board import Board


class Engine(ABC):
    """
    Abstract class containing methods for Engine
    """

    __slots__ = ()

    @abstractmethod
    def get_computer_move(self, board: 'Board') -> Move:
        """
        Method used to return best computer move possible
        :param board: Board instance
        :return: the best computer Move instance
        """
        pass
