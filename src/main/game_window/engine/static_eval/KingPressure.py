import math
from typing import TYPE_CHECKING

from numba import jit
from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil

if TYPE_CHECKING:
    from game_window.board.Board import Board


class KingPressure:
    """
    Class containing methods to evaluate king pressure
    """

    __slots__ = ()

    @staticmethod
    def evaluate_king_pressure(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate pressure on king.
        :param board: Board instance
        :param favor_color: int value of color in favor of which we evaluate position
        :return: int evaluation
        """
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)
        pressure_on_enemy_king = KingPressure.evaluate_king_pressure_only_for_color(board, favor_color)
        pressure_on_my_king = KingPressure.evaluate_king_pressure_only_for_color(board, enemy_color)
        evaluation: int = int(pressure_on_enemy_king - pressure_on_my_king)

        return evaluation

    @staticmethod
    @jit(forceobj=True)
    def evaluate_king_pressure_only_for_color(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate distance of pieces to the enemy king
        :param favor_color: int value of color
        :param board: Board instance
        :return: int value of evaluation
        """
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)
        board_array: ndarray[int] = board.get_board_array()

        enemy_king_pos = KingUtil.find_friendly_king_squares(board_array, enemy_color)
        enemy_king_x = math.floor(enemy_king_pos / 8)
        enemy_king_y = enemy_king_pos - 8 * enemy_king_x
        score_accumulator = 0

        for pos in range(BoardEnum.BOARD_SIZE.value):
            if ColorManager.get_piece_color(board_array[pos]) != favor_color:
                continue
            my_piece_x = math.floor(pos / 8)
            my_piece_y = pos - 8 * my_piece_x

            x_diff = enemy_king_x - my_piece_x
            y_diff = enemy_king_y - my_piece_y

            distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
            score = 8 * math.sqrt(2) - distance
            score_accumulator += score
        return score_accumulator
