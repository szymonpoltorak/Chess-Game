from typing import TYPE_CHECKING

from game_window.engine.Evaluation import Evaluation
from game_window.engine.static_eval.KingPressure import KingPressure
from game_window.engine.static_eval.LightPiecesEval import LightPiecesEval
from game_window.engine.static_eval.PawnEval import PawnEval
from game_window.engine.static_eval.RookEval import RookEval
from game_window.engine.static_eval.StaticEvaluation import StaticEvaluation
from game_window.engine.static_eval.StaticEvaluator import StaticEvaluator

if TYPE_CHECKING:
    from game_window.board.Board import Board


class Evaluator(Evaluation):
    """
    Class containing methods to evaluate position
    """

    __slots__ = "__static_evaluator"

    def __init__(self) -> None:
        self.__static_evaluator: StaticEvaluation = StaticEvaluator()

    @staticmethod
    def debug_evaluate_position(board: 'Board', favor_color: int) -> float:
        """
        Debug Method
        :param board:
        :param favor_color:
        :return:
        """
        print("For BLACK:") if favor_color == 16 else print("For WHITE:")

        material_eval: float = StaticEvaluator.evaluate_pieces_on_board(board, favor_color)
        center_possession_eval: float = StaticEvaluator.evaluate_center_possession(board, favor_color)

        light_dev_eval: float = LightPiecesEval.evaluate_light_pieces_walked(board, favor_color)
        bishops: float = LightPiecesEval.evaluate_bishops(board, favor_color)

        king_pressure: float = KingPressure.evaluate_king_pressure(board, favor_color)

        free_lines: float = RookEval.evaluate_free_lines_for_rooks(board, favor_color)

        chains: float = PawnEval.evaluate_pawn_chains(board, favor_color)

        print(f"\tmaterialEval = {material_eval}\n\tcenterPossessionEval = {center_possession_eval}\n\t"
              f"lightDevEval = {light_dev_eval}\n\tkingPressure = {king_pressure}")
        print(f"\tbishops = {bishops}\n\tfree lines = {free_lines}\n\tpawn chains = {chains}")
        print(f"\tconnection = {RookEval.eval_rook_connection(board, favor_color)}")

        total_eval: float = material_eval + center_possession_eval + light_dev_eval + king_pressure + free_lines + chains + bishops
        print(f"\tTotal = {total_eval}\n")

        return total_eval

    def evaluate_position(self, board: 'Board', favor_color: int) -> float:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: int value of favor_color in favor of which we evaluate position
        :return: float evaluation
        """
        total_eval: float = self.__static_evaluator.evaluate_static_position(board, favor_color)

        return total_eval
