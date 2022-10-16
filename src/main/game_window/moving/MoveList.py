from dataclasses import dataclass

from numpy import ndarray

from game_window.moving.Move import Move


@dataclass(slots=True, eq=True, order=True, unsafe_hash=True)
class MoveList:
    moves: ndarray[Move]
    free_index: int
