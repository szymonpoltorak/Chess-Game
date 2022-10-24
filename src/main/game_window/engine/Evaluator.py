from typing import TYPE_CHECKING

from numpy.random import randint

if TYPE_CHECKING:
    from game_window.Board import Board


class Evaluator:
    @staticmethod
    def evaluate_position(board: 'Board'):
        value = randint(0, 300)
        return value
