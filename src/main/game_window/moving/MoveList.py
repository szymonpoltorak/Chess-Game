from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import TYPE_CHECKING

from numpy import dtype
from numpy import generic
from numpy import ndarray

from exceptions.NullArgumentException import NullArgumentException
from game_window.moving.Move import Move
from game_window.moving.MoveSortUtil import MoveSortUtil

if TYPE_CHECKING:
    from game_window.board.Board import Board


@dataclass(slots=True, order=True, unsafe_hash=True)
class MoveList:
    """
    Class containing the list of item
    """
    moves: ndarray[Move, dtype[generic]]
    __size: int = field(default=0)

    def append(self, move: Move) -> None:
        """
        Method used to append new move to the MoveList
        :param move: Move instance
        """
        if move is None:
            raise NullArgumentException("WHY YOU ADD NULL MOVE TO MOVE LIST ?")
        self.moves[self.__size] = move
        self.__size += 1

    def is_empty(self) -> bool:
        """
        Method used to check if move list is empty
        :return: bool
        """
        return self.__size == 0

    def sort(self, board: 'Board') -> None:
        """
        Method used to sort list of item based on
        :return: None
        """
        sorted_moves: list[Move, ...] = sorted(self.moves, key=lambda item: MoveSortUtil.count_moves_score(item, board),
                                               reverse=True)
        index: int = 0

        for move in sorted_moves:
            if move is None:
                break
            self.moves[index] = move
            index += 1

    def __iter__(self) -> Any:
        return self.moves.__iter__()

    def __contains__(self, move: Move) -> bool:
        return move in self.moves
