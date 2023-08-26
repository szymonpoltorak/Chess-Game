from abc import ABC
from abc import abstractmethod
from typing import TYPE_CHECKING

from src.main.game_window.moving.generation.data.MoveList import MoveList

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class PawnGenerator(ABC):
    """
    Abstract class for Pawn Generation classes
    """

    __slots__ = ()

    @abstractmethod
    def generate_pawn_moves(self, moves_list: MoveList, piece: int, color: int, board: 'Board', start_square: int,
                            captures_only: bool) -> None:
        """
        Static method to generate moves_list for pawns
        :param captures_only: decides if method should generate every legal move or captures only
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start end_square index
        :return: None
        """
        pass
