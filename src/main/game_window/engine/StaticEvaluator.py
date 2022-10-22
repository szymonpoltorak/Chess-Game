import math
from typing import TYPE_CHECKING

from numba import jit
from numpy import array
from numpy import int8
from numpy import ndarray

from game_window.CheckUtil import CheckUtil
from game_window.ColorManager import ColorManager
from game_window.engine.EvalUtil import EvalUtil
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.MoveUtil import MoveUtil

if TYPE_CHECKING:
    from game_window.Board import Board


class StaticEvaluator:
    @staticmethod
    @jit(forceobj=True)
    def evaluate_static_position(board: 'Board', favor_color: int) -> int:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: int value of color in favor of which we evaluate position
        :return: int evaluation
        """
        material_eval = StaticEvaluator.evaluate_pieces_on_board(board, favor_color)
        center_possession_eval = StaticEvaluator.evaluate_center_possession(board, favor_color)
        light_dev_eval = StaticEvaluator.evaluate_light_pieces_walked(board, favor_color)
        king_pressure = StaticEvaluator.evaluate_king_pressure(board, favor_color)
        bishops = StaticEvaluator.evaluate_bishops(board, favor_color)
        free_lines = StaticEvaluator.evaluate_free_lines_for_rooks(board, favor_color)

        static_eval = material_eval + center_possession_eval + light_dev_eval + king_pressure + free_lines + bishops

        return static_eval

    @staticmethod
    @jit(forceobj=True)
    def evaluate_pieces_on_board(board: 'Board', favor_color: int) -> int:
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
            points: int = EvalUtil.get_piece_point_value(piece_value)

            evaluation += points if pieces_color == favor_color else -points
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
        board_array: ndarray[int] = board.get_board_array()
        favorable_accumulator: int = 0
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)
        unfavorable_accumulator: int = 0
        favor_light_walked: int = 0
        un_favor_light_walked: int = 0

        light_pieces_positions: dict = {
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
        if favor_light_walked != 4 and EvalUtil.is_queen_on_start_position(favor_color, board):
            favor_light_walked -= 2 * EvalEnum.WALKED.value
        if un_favor_light_walked != 4 and EvalUtil.is_queen_on_start_position(enemy_color, board):
            favor_light_walked -= 2 * EvalEnum.WALKED.value
        return favorable_accumulator - unfavorable_accumulator

    @staticmethod
    def evaluate_king_pressure(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate pressure on king.
        :param board: Board instance
        :param favor_color: int value of color in favor of which we evaluate position
        :return: int evaluation
        """
        pressure_on_enemy_king = StaticEvaluator.evaluate_king_pressure_only_for_color(board, favor_color)
        pressure_on_my_king = StaticEvaluator.evaluate_king_pressure_only_for_color(board,
                                                                                    ColorManager.get_opposite_piece_color(
                                                                                        favor_color))
        pressure = pressure_on_enemy_king - pressure_on_my_king

        return int(pressure)

    @staticmethod
    @jit(forceobj=True)
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
    @jit(forceobj=True)
    def evaluate_center_possession(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate a center possession
        :param favor_color:
        :param board: Board instance
        :return: int value of evaluation
        """
        evaluation: int = 0
        board_array: ndarray[int] = board.get_board_array()

        for center_square in BoardEnum.CENTER_SQUARES.value:
            piece: int = board_array[center_square]

            if piece == PiecesEnum.NONE.value:
                continue
            piece_color: int = ColorManager.get_piece_color(piece)

            if center_square in BoardEnum.CENTER_SIDE_SQUARES.value:
                evaluation += EvalUtil.return_proper_evaluation_signed_value(board, EvalEnum.SIDE_CENTER.value,
                                                                             piece_color)
            if center_square in BoardEnum.CENTER_MAIN_SQUARES.value:
                evaluation += EvalUtil.return_proper_evaluation_signed_value(board, EvalEnum.MAIN_CENTER.value,
                                                                             piece_color)
        return EvalUtil.return_proper_evaluation_signed_value(board, evaluation, favor_color)

    @staticmethod
    @jit(forceobj=True)
    def evaluate_bishops(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate if player has a pair of bishops.
        :param board: Board instance
        :param favor_color: color which is now evaluating for
        :return: int value of evaluation
        """
        evaluation: int = 0
        board_array: ndarray[int] = board.get_board_array()
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
        return EvalUtil.return_proper_evaluation_signed_value(board, evaluation, favor_color)

    @staticmethod
    @jit(forceobj=True)
    def evaluate_free_lines_for_rooks(board: 'Board', favor_color: int):
        """
        Methods used to evaluate free lines for rooks
        :param board: Board instance
        :param favor_color: color which is now evaluating for
        :return: int value of evaluation
        """
        board_array: ndarray[int] = board.get_board_array()
        evaluation: int = 0

        for square, piece in enumerate(board_array):
            piece_color: int = ColorManager.get_piece_color(piece)
            piece_value: int = piece - piece_color

            if piece_value == PiecesEnum.ROOK.value and MoveUtil.is_it_free_line(board, square, MoveEnum.TOP_STEP.value,
                                                                                 MoveEnum.TOP_DIR.value):
                evaluation += EvalUtil.return_proper_evaluation_signed_value(board, EvalEnum.FREE_LINE.value,
                                                                             piece_color)
            if piece_value == PiecesEnum.ROOK.value and MoveUtil.is_it_free_line(board, square,
                                                                                 MoveEnum.LEFT_STEP.value,
                                                                                 MoveEnum.LEFT_DIR.value):
                evaluation += EvalUtil.return_proper_evaluation_signed_value(board, EvalEnum.FREE_LINE.value,
                                                                             piece_color)
        return EvalUtil.return_proper_evaluation_signed_value(board, evaluation, favor_color)
