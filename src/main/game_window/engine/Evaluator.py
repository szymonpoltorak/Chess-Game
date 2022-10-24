from typing import TYPE_CHECKING

from numba import jit

from game_window.engine.static_eval.KingPressure import KingPressure
from game_window.engine.static_eval.LightPiecesEval import LightPiecesEval
from game_window.engine.static_eval.PawnEval import PawnEval
from game_window.engine.static_eval.RookEval import RookEval
from game_window.engine.static_eval.StaticEvaluator import StaticEvaluator

if TYPE_CHECKING:
    from game_window.board.Board import Board


class Evaluator:
    """
    Class containing methods to evaluate position
    """

    @staticmethod
    def debug_evaluate_position(board: 'Board', favor_color: int) -> int:
        """
        Debug Method
        :param board:
        :param favor_color:
        :return:
        """
        print("For BLACK:") if favor_color == 16 else print("For WHITE:")

        material_eval = StaticEvaluator.evaluate_pieces_on_board(board, favor_color)
        center_possession_eval = StaticEvaluator.evaluate_center_possession(board, favor_color)
        light_dev_eval = LightPiecesEval.evaluate_light_pieces_walked(board, favor_color)
        king_pressure = KingPressure.evaluate_king_pressure(board, favor_color)
        bishops = LightPiecesEval.evaluate_bishops(board, favor_color)
        free_lines = RookEval.evaluate_free_lines_for_rooks(board, favor_color)
        chains = PawnEval.evaluate_pawn_chains(board, favor_color)

        print(f"\tmaterialEval = {material_eval}\n\tcenterPossessionEval = {center_possession_eval}\n\tlightDevEval = {light_dev_eval}\n\tkingPressure = {king_pressure}")
        print(f"\tbishops = {bishops}\n\tfree lines = {free_lines}\n\tpawn chains = {chains}")

        total_eval = material_eval + center_possession_eval + light_dev_eval + king_pressure + free_lines + chains + bishops
        print(f"\tTotal = {total_eval}\n")

        return total_eval

    @staticmethod
    @jit(forceobj=True)
    def evaluate_position(board: 'Board', favor_color: int) -> int:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: int value of color in favor of which we evaluate position
        :return: int evaluation
        """

        total_eval = StaticEvaluator.evaluate_static_position(board, favor_color)

        return total_eval
