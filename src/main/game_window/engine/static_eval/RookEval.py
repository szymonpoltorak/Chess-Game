from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.engine.static_eval.StaticEvalUtil import StaticEvalUtil
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class RookEval:
    """
    Class containing methods to evaluate rooks
    """

    __slots__ = ()

    @staticmethod
    def get_free_line_eval(board: 'Board', start_square: int) -> float:
        """
        Method used to get free lines evals
        :param board: Board instance
        :param start_square: int starting square of a rook
        :return: float
        """
        horizontal_eval: float = RookEval.get_horizontal_eval(start_square, board)
        vertical_eval: float = RookEval.get_vertical_eval(start_square, board)

        return horizontal_eval + vertical_eval

    @staticmethod
    def evaluate_free_lines_for_rooks(board: 'Board', favor_color: int) -> float:
        """
        Methods used to evaluate free lines for rooks
        :param favor_color: float value of color
        :param board: Board instance
        :return: float value of evaluation
        """
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        evaluation: float = 0

        for square, piece in enumerate(board_array):
            piece_color: int = ColorManager.get_piece_color(piece)
            piece_value: int = piece - piece_color

            if piece_value == PiecesEnum.ROOK.value:
                free_line_eval: float = RookEval.get_free_line_eval(board, square)
                evaluation += StaticEvalUtil.return_proper_evaluation_signed_value(board, free_line_eval, piece_color)
        return evaluation

    @staticmethod
    def get_horizontal_eval(start_square: int, board: 'Board') -> float:
        """
        Method used to evaluate horizontal lines of rooks
        :param start_square: starting square of a rook
        :param board: Board instance
        :return: float
        """
        left_step: int = -1
        right_step: int = 1
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        distances: ndarray[int, dtype[int8]] = board.distances()
        distance_to_left: int = distances[start_square][3]
        distance_to_right: int = distances[start_square][4]
        left_border: int = start_square + left_step * distance_to_left - 1
        right_border: int = start_square + right_step * distance_to_right + 1

        for index in range(start_square - 1, left_border, left_step):
            if distance_to_left == 0:
                break

            if board_array[index] != PiecesEnum.NONE.value:
                return 0

        for index in range(start_square + 1, right_border, right_step):
            if distance_to_right == 0:
                break

            if board_array[index] != PiecesEnum.NONE.value:
                return 0
        return EvalEnum.FREE_LINE.value

    @staticmethod
    def get_vertical_eval(start_square: int, board: 'Board') -> float:
        """
        Method used to evaluate vertical lines of rooks
        :param start_square: starting square of a rook
        :param board: Board instance
        :return: float
        """
        top_step: int = -8
        bottom_step: int = 8
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        distances: ndarray[int, dtype[int8]] = board.distances()
        distance_to_top: int = distances[start_square][1]
        distance_to_bottom: int = distances[start_square][6]
        top_border: int = start_square + top_step * distance_to_top - 1
        bottom_border: int = start_square + bottom_step * distance_to_bottom + 1

        for index in range(start_square - 8, top_border, top_step):
            if distance_to_top == 0:
                break

            if board_array[index] != PiecesEnum.NONE.value:
                return 0

        for index in range(start_square + 8, bottom_border, bottom_step):
            if distance_to_bottom == 0:
                break

            if board_array[index] != PiecesEnum.NONE.value:
                return 0
        return EvalEnum.FREE_LINE.value
