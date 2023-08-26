from abc import ABC
from abc import abstractmethod
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board
from src.main.game_window.moving.generation.data.Move import Move


class MoveList(ABC):
    """
    Abstract class of a MoveList representation
    """

    __slots__ = ()

    @abstractmethod
    def append(self, move: Move) -> None:
        """
        Method used to append new move to the Moves
        :param move: Move instance
        """
        pass

    @abstractmethod
    def size(self) -> int:
        """
        Method used to return the size of move list
        :return: int value of size
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Method used to check if move list is empty
        :return: bool
        """
        pass

    @abstractmethod
    def sort(self, board: 'Board') -> None:
        """
        Method used to sort list of item based on
        :return: None
        """
        pass

    @abstractmethod
    def __iter__(self) -> Any:
        pass

    @abstractmethod
    def __getitem__(self, item: int) -> Any:
        pass

    @abstractmethod
    def __contains__(self, move: Move) -> bool:
        pass

    @abstractmethod
    def __copy__(self) -> Any:
        pass
