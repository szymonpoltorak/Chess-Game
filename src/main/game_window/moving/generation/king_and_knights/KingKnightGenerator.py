from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from src.main.game_window.moving.generation.data.MoveList import MoveList

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class KingKnightGenerator(ABC):
    """
    Abstract class for Knights and Kings generation
    """

    @abstractmethod
    def generate_moves_for_knight_and_king(self, moves_list: MoveList, piece: int, color: int, board: 'Board',
                                           start_square: int, captures_only: bool) -> None:
        """
        Static method used to generate moves_list for knights and kings
        :param captures_only: decides if method should generate every legal move or captures only
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of piece_square
        :param color: int value of color to move
        :param board: board instance
        :param start_square: int index of current end_square
        :return: None
        """
        pass
