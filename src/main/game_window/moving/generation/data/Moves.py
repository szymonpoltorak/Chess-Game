from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import TYPE_CHECKING

from numpy import asarray
from numpy import dtype
from numpy import generic
from numpy import ndarray

from exceptions.NullArgumentException import NullArgumentException
from game_window.moving.generation.data.MoveList import MoveList
from game_window.moving.generation.data.Move import Move
from game_window.moving.MoveSortUtil import MoveSortUtil

if TYPE_CHECKING:
    from game_window.board.Board import Board


@dataclass(slots=True, order=True, unsafe_hash=True)
class Moves(MoveList):
    """
    Class containing the list of item
    """
    __moves: ndarray[Move, dtype[generic]]
    __size: int = field(default=0)

    def append(self, move: Move) -> None:
        """
        Method used to append new move to the Moves
        :param move: Move instance
        """
        if move is None:
            raise NullArgumentException("WHY YOU ADD NULL MOVE TO MOVE LIST ?")
        self.__moves[self.__size] = move
        self.__size += 1

    def size(self) -> int:
        """
        Method used to return the size of move list
        :return: int value of size
        """
        return self.__size

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
        sorted_moves: list[Move] = sorted(self.__moves, key=lambda item: MoveSortUtil.count_moves_score(item, board),
                                          reverse=True)
        self.__moves = asarray(sorted_moves)

    def __iter__(self) -> Any:
        return self.__moves.__iter__()

    def __getitem__(self, item: int) -> Any:
        return self.__moves[item]

    def __contains__(self, move: Move) -> bool:
        return move in self.__moves
