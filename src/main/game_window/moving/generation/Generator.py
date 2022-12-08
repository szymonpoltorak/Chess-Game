from abc import ABC
from typing import TYPE_CHECKING

from game_window.moving.generation.data.MoveList import MoveList

if TYPE_CHECKING:
    from game_window.board.Board import Board


class Generator(ABC):
    """
    Abstract class containing abstract methods for move generation
    """

    __slots__ = ()

    def generate_legal_moves(self, color_to_move: int, board: 'Board', captures_only: bool = False) -> MoveList:
        """
        Method used to generate legal __moves for current position for given player
        :param captures_only: decides if method should generate every legal move or captures only
        :param color_to_move: player color int
        :param board: Board instance
        :return: MoveList
        """
        pass
