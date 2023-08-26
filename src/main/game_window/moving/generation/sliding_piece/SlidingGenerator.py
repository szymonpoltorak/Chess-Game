from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from src.main.game_window.moving.generation.data.MoveList import MoveList

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class SlidingGenerator(ABC):
    """
    Abstract class for Sliding Generation
    """

    __slots__ = ()

    @abstractmethod
    def generate_sliding_piece_moves(self, piece: int, start_square: int, moves_list: MoveList, color: int,
                                     board: 'Board', captures_only: bool) -> None:
        """
        Static method used to generate moves_list for sliding pieces
        :param captures_only: decides if method should generate every legal move or captures only
        :param piece: int value of piece_square
        :param start_square: int index of current end_square
        :param moves_list: list of moves_list
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        pass
