from typing import TYPE_CHECKING

from numba import jit
from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.engine.static_eval.KingPressure import KingPressure
from game_window.engine.static_eval.LightPiecesEval import LightPiecesEval
from game_window.engine.static_eval.PawnEval import PawnEval
from game_window.engine.static_eval.RookEval import RookEval
from game_window.engine.static_eval.StaticEvalUtil import StaticEvalUtil
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class StaticEvaluator:
    """
    Class containing methods for static evaluation
    """

    __slots__ = ()

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
        light_dev_eval = LightPiecesEval.evaluate_light_pieces_walked(board, favor_color)
        king_pressure = KingPressure.evaluate_king_pressure(board, favor_color)
        bishops = LightPiecesEval.evaluate_bishops(board, favor_color)
        free_lines = RookEval.evaluate_free_lines_for_rooks(board, favor_color)
        chains = PawnEval.evaluate_pawn_chains(board, favor_color)

        static_eval = material_eval + center_possession_eval + light_dev_eval + king_pressure + free_lines + bishops
        static_eval += chains

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
            points: int = StaticEvalUtil.get_piece_point_value(piece_value)

            evaluation += points if pieces_color == board.get_engine_color() else -points
        return evaluation

    @staticmethod
    @jit(forceobj=True)
    def evaluate_center_possession(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate a center possession
        :param favor_color: int value of color
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
                evaluation += StaticEvalUtil.return_proper_evaluation_signed_value(board, EvalEnum.SIDE_CENTER.value,
                                                                                   piece_color)
            if center_square in BoardEnum.CENTER_MAIN_SQUARES.value:
                evaluation += StaticEvalUtil.return_proper_evaluation_signed_value(board, EvalEnum.MAIN_CENTER.value,
                                                                                   piece_color)
        return evaluation
