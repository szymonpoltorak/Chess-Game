import math
from typing import TYPE_CHECKING

from numpy import array
from numpy import int8
from numpy import ndarray

from game_window.CheckUtil import CheckUtil
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.Board import Board


class Evaluator:
    @staticmethod
    def debug_evaluate_position(board: 'Board', favor_color: int) -> int:
        print("For BLACK:") if favor_color == 16 else print("For WHITE:")

        material_eval = 2 * Evaluator.sum_pieces_on_board(board, favor_color)
        center_possession_eval = Evaluator.evaluate_center_possession(board, favor_color)
        light_dev_eval = Evaluator.evaluate_light_pieces_walked(board, favor_color)
        king_pressure = Evaluator.evaluate_king_pressure(board, favor_color)

        print(f"\tmaterialEval = {material_eval}\n\tcenterPossessionEval = {center_possession_eval}\n\tlightDevEval = {light_dev_eval}\n\tkingPressure = {king_pressure}")

        total_eval = material_eval + center_possession_eval + light_dev_eval + king_pressure
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
        material_eval = 2 * Evaluator.sum_pieces_on_board(board, favor_color)
        center_possession_eval = Evaluator.evaluate_center_possession(board, favor_color)
        light_dev_eval = Evaluator.evaluate_light_pieces_walked(board, favor_color)
        king_pressure = Evaluator.evaluate_king_pressure(board, favor_color)

        total_eval = material_eval + center_possession_eval + light_dev_eval + king_pressure

        return total_eval if favor_color == board.get_engine_color() else -total_eval

    @staticmethod
    def sum_pieces_on_board(board: 'Board', favor_color: int) -> int:
        """
        Method used to sum value of pieces on board and return this sum as evaluation
        :param favor_color:
        :param board: Board instance
        :return: int value of evaluation
        """
        evaluation: int = 0
        board_array: ndarray[int] = board.get_board_array()

        for square in board_array:
            if square == 0:
                continue

            pieces_color: int = ColorManager.get_piece_color(square)
            piece_value: int = square - pieces_color
            points: int = Evaluator.get_piece_point_value(piece_value)
            evaluation += points if pieces_color == favor_color else -points
        return evaluation

    @staticmethod
    def evaluate_light_pieces_walked(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate if light pieces are walked from their starting position
        :param favor_color:
        :param board: Board instance
        :return: int value of evaluation
        """
        pieces = array([PiecesEnum.KNIGHT.value, PiecesEnum.BISHOP.value, PiecesEnum.BISHOP.value, PiecesEnum.KNIGHT.value])
        engine_color: int = board.get_engine_color()
        player_color: int = board.get_player_color()
        board_array: ndarray[int] = board.get_board_array()

        light_pieces_positions: dict = {
            engine_color: array([1, 2, 5, 6], dtype=int8),
            player_color: array([57, 58, 61, 62], dtype=int8),
        }
        favorable_accumulator = 0

        for i in range(0, 4):
            position = light_pieces_positions[favor_color][i]

            if board_array[position] == favor_color | pieces[i]:
                favorable_accumulator -= EvalEnum.WALKED.value
            else:
                favorable_accumulator += EvalEnum.WALKED.value

        enemy_color = ColorManager.get_opposite_piece_color(favor_color)
        unfavorable_accumulator = 0

        for i in range(0, 4):
            position = light_pieces_positions[enemy_color][i]

            if board_array[position] == enemy_color | pieces[i]:
                unfavorable_accumulator -= EvalEnum.WALKED.value
            else:
                unfavorable_accumulator += EvalEnum.WALKED.value

        return favorable_accumulator - unfavorable_accumulator

    @staticmethod
    def evaluate_king_pressure(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate pressure on king.
        :param board: Board instance
        :param favor_color: int value of color in favor of which we evaluate position
        :return: int evaluation
        """
        pressure_on_enemy_king = Evaluator.evaluate_king_pressure_only_for_color(board, favor_color)
        pressure_on_my_king = Evaluator.evaluate_king_pressure_only_for_color(board,
                                                                              ColorManager.get_opposite_piece_color(
                                                                                  favor_color))
        net_pressure = pressure_on_enemy_king - pressure_on_my_king

        return int(net_pressure)

    @staticmethod
    def evaluate_king_pressure_only_for_color(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate distance of pieces to the enemy king
        :param favor_color:
        :param board: Board instance
        :return: int value of evaluation
        """
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)
        board_array: ndarray[int] = board.get_board_array()

        enemy_king_pos = CheckUtil.find_friendly_king_squares(board_array, enemy_color)
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

    @staticmethod
    def return_proper_evaluation_signed_value(board: 'Board', evaluation: int, favor_color: int) -> int:
        """
        Method used to return a proper mark of evaluation based on favor_color to move
        :param favor_color:
        :param board: Board instance
        :param evaluation: int value of evaluation
        :return: int value with proper sign
        """
        return evaluation if favor_color == board.get_engine_color() else -evaluation

    @staticmethod
    def get_piece_point_value(piece_value: int) -> int:
        """
        Method used to get proper eval value of a piece
        :param piece_value: int value of piece
        :return: int value of piece eval
        """
        pieces_dict = {
            PiecesEnum.KNIGHT.value: EvalEnum.KNIGHT.value,
            PiecesEnum.BISHOP.value: EvalEnum.BISHOP.value,
            PiecesEnum.ROOK.value: EvalEnum.ROOK.value,
            PiecesEnum.QUEEN.value: EvalEnum.QUEEN.value,
            PiecesEnum.PAWN.value: EvalEnum.PAWN.value,
            PiecesEnum.KING.value: EvalEnum.KING.value
        }
        return pieces_dict[piece_value]

    @staticmethod
    def evaluate_center_possession(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate a center possession
        :param favor_color:
        :param board: Board instance
        :return: int value of evaluation
        """
        evaluation: int = 0
        board_array: ndarray[int] = board.get_board_array()

        for center_square in range(26, 30):
            if board_array[center_square] == PiecesEnum.NONE.value:
                continue
            piece_color: int = ColorManager.get_piece_color(board_array[center_square])
            evaluation += EvalEnum.CENTER.value if piece_color == board.get_engine_color() else -EvalEnum.CENTER.value

        for center_square in range(34, 38):
            if board_array[center_square] == PiecesEnum.NONE.value:
                continue
            piece_color: int = ColorManager.get_piece_color(board_array[center_square])
            evaluation += EvalEnum.CENTER.value if piece_color == board.get_engine_color() else -EvalEnum.CENTER.value
        return Evaluator.return_proper_evaluation_signed_value(board, evaluation, favor_color)
