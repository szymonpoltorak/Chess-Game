from typing import TYPE_CHECKING

from game_window.engine.StaticEvaluator import StaticEvaluator

if TYPE_CHECKING:
    from game_window.Board import Board


class Evaluator:
    @staticmethod
    def debug_evaluate_position(board: 'Board', favor_color: int) -> int:
        print("For BLACK:") if favor_color == 16 else print("For WHITE:")

        material_eval = StaticEvaluator.sum_pieces_on_board(board, favor_color)
        center_possession_eval = StaticEvaluator.evaluate_center_possession(board, favor_color)
        light_dev_eval = StaticEvaluator.evaluate_light_pieces_walked(board, favor_color)
        king_pressure = StaticEvaluator.evaluate_king_pressure(board, favor_color)
        bishops = StaticEvaluator.evaluate_bishops(board, favor_color)
        free_lines = StaticEvaluator.evaluate_free_lines_for_rooks(board, favor_color)

        print(f"\tmaterialEval = {material_eval}\n\tcenterPossessionEval = {center_possession_eval}\n\tlightDevEval = {light_dev_eval}\n\tkingPressure = {king_pressure}")
        print(f"\tbishops = {bishops}\n\tfree lines = {free_lines}")

        total_eval = material_eval + center_possession_eval + light_dev_eval + king_pressure + free_lines
        print(f"\tTotal = {total_eval}\n")

        return total_eval if favor_color == board.get_engine_color() else -total_eval

    @staticmethod
    def evaluate_position(board: 'Board', favor_color: int) -> int:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: int value of color in favor of which we evaluate position
        :return: int evaluation
        """

        total_eval = StaticEvaluator.evaluate_static_position(board, favor_color)

        return total_eval
