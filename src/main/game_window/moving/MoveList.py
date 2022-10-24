from dataclasses import dataclass

from numpy import ndarray

from game_window.moving.Move import Move


@dataclass(slots=True, order=True, unsafe_hash=True)
class MoveList:
    """
    Class containing the list of moves
    """
    moves: ndarray[Move]
    free_index: int

    def append(self, move: Move) -> None:
        """
        Method used to append new move to the MoveList
        :param move: Move instance
        """
        self.moves[self.free_index] = move
        self.free_index += 1
