from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
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
    def evaluate_static_position(board: 'Board', favor_color: int) -> float:
        """
        Method used to return an evaluation of starting position
        :param board: Board instance
        :param favor_color: float value of color in favor of which we evaluate position
        :return: float evaluation
        """
        material_eval: float = StaticEvaluator.evaluate_pieces_on_board(board, favor_color)
        center_possession_eval: float = StaticEvaluator.evaluate_center_possession(board, favor_color)
        light_dev_eval: float = LightPiecesEval.evaluate_light_pieces_walked(board, favor_color)
        king_pressure: float = KingPressure.evaluate_king_pressure(board, favor_color)
        bishops: float = LightPiecesEval.evaluate_bishops(board, favor_color)
        free_lines: float = RookEval.evaluate_free_lines_for_rooks(board, favor_color)
        chains: float = PawnEval.evaluate_pawn_chains(board, favor_color)

        static_eval: float = material_eval + center_possession_eval + light_dev_eval + king_pressure + free_lines + bishops
        static_eval += chains

        return static_eval

    @staticmethod
    def evaluate_pieces_on_board(board: 'Board', favor_color: int) -> float:
        """
        Method used to sum value of pieces on board and return this sum as evaluation
        :param favor_color:
        :param board: Board instance
        :return: float value of evaluation
        """
        evaluation: float = 0
        board_array: ndarray[int, dtype[int8]] = board.board_array()

        for square, piece in enumerate(board_array):
            if piece == 0:
                continue
            pieces_color: int = ColorManager.get_piece_color(piece)
            piece_value: int = piece - pieces_color
            points: float = StaticEvalUtil.get_piece_point_value(piece_value)
            points += StaticEvalUtil.get_pieces_square_points(piece_value, pieces_color, square, board)

            evaluation += points if pieces_color == board.engine_color() else -points
        return evaluation

    @staticmethod
    def evaluate_center_possession(board: 'Board', favor_color: int) -> float:
        """
        Method used to evaluate a center possession
        :param favor_color: float value of color
        :param board: Board instance
        :return: float value of evaluation
        """
        evaluation: float = 0
        board_array: ndarray[int, dtype[int8]] = board.board_array()

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
