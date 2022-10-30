from typing import TYPE_CHECKING, Dict

from numba import jit
from numpy import array, dtype
from numpy import int8
from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.engine.static_eval.StaticEvalUtil import StaticEvalUtil
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class LightPiecesEval:
    """
    Class containing methods to evaluate light pieces
    """

    __slots__ = ()

    @staticmethod
    @jit(forceobj=True)
    def evaluate_bishops(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate if player has a pair of bishops.
        :param favor_color: int value of color
        :param board: Board instance
        :return: int value of evaluation
        """
        evaluation: int = 0
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        engine_color: int = board.get_engine_color()
        player_color: int = board.get_player_color()
        engine_bishops: int = 0
        player_bishops: int = 0

        for square, piece in enumerate(board_array):
            if piece == PiecesEnum.NONE.value:
                continue

            if piece == engine_color | PiecesEnum.BISHOP.value:
                engine_bishops += 1
            elif piece == player_color | PiecesEnum.BISHOP.value:
                player_bishops += 1
        if engine_bishops >= 2:
            evaluation += EvalEnum.BISHOP_PAIR.value
        if player_bishops >= 2:
            evaluation -= EvalEnum.BISHOP_PAIR.value
        return evaluation

    @staticmethod
    @jit(forceobj=True)
    def evaluate_light_pieces_walked(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate if light pieces are walked from their starting position
        :param favor_color:
        :param board: Board instance
        :return: int value of evaluation
        """
        pieces = array([PiecesEnum.KNIGHT.value, PiecesEnum.BISHOP.value, PiecesEnum.BISHOP.value, PiecesEnum.KNIGHT.value])
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        favorable_accumulator: int = 0
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)
        unfavorable_accumulator: int = 0
        favor_light_walked: int = 0
        un_favor_light_walked: int = 0

        light_pieces_positions: Dict[int, ndarray[int, dtype[int8]]] = {
            board.get_engine_color(): array([1, 2, 5, 6], dtype=int8),
            board.get_player_color(): array([57, 58, 61, 62], dtype=int8),
        }

        for i in range(0, 4):
            position = light_pieces_positions[favor_color][i]
            enemy_position = light_pieces_positions[enemy_color][i]

            if board_array[position] == favor_color | pieces[i]:
                favorable_accumulator -= EvalEnum.WALKED.value
            else:
                favor_light_walked += 1
                favorable_accumulator += EvalEnum.WALKED.value

            if board_array[enemy_position] == enemy_color | pieces[i]:
                unfavorable_accumulator -= EvalEnum.WALKED.value
            else:
                un_favor_light_walked += 1
                unfavorable_accumulator += EvalEnum.WALKED.value
        if favor_light_walked != 4 and StaticEvalUtil.is_queen_on_start_position(favor_color, board):
            favor_light_walked -= 2 * EvalEnum.WALKED.value
        if un_favor_light_walked != 4 and StaticEvalUtil.is_queen_on_start_position(enemy_color, board):
            favor_light_walked -= 2 * EvalEnum.WALKED.value

        evaluation: int = favorable_accumulator - unfavorable_accumulator
        return evaluation
