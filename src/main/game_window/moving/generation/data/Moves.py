from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import TYPE_CHECKING

from numpy import array, argsort
from numpy.typing import NDArray

from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.moving.MoveSortUtil import MoveSortUtil
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.data.MoveList import MoveList

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


@dataclass(slots=True, order=True, unsafe_hash=True)
class Moves(MoveList):
    """
    Class containing the list of item
    """
    __moves: NDArray[Move]
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
        Method used to sort list of item based on move score
        :param board: Board instance
        :return: None
        """
        move_scores: NDArray[float] = array([MoveSortUtil.count_moves_score(item, board)
                                             for item in self.__moves])
        sorted_indices: NDArray[int] = argsort(move_scores)[::-1]

        self.__moves = self.__moves[sorted_indices]

    def __iter__(self) -> Any:
        return self.__moves.__iter__()

    def __getitem__(self, item: int) -> Any:
        return self.__moves[item]

    def __contains__(self, move: Move) -> bool:
        return move in self.__moves

    def __copy__(self) -> Any:
        return Moves(self.__moves.copy(), self.__size)
