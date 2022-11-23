from typing import TYPE_CHECKING

from game_window.board.BoardUtil import BoardUtil
from game_window.ColorManager import ColorManager
from game_window.engine.static_eval.StaticEvalUtil import StaticEvalUtil
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveSortUtil:
    """
    Class containing util methods for move list class
    """

    @staticmethod
    def count_moves_score(move: Move, board: 'Board') -> int:
        """
        Method used to make early evaluation to sort __moves so to make search faster
        :param move: Move to evaluate
        :param board: Board instance
        :return: int value of evaluation
        """
        if move is None:
            return -999_999

        score: int = 0
        target_square: int = move.get_end_square()
        target_piece: int = board.board_array()[target_square]
        target_color: int = ColorManager.get_piece_color(target_piece)
        target_piece_value: int = target_piece - target_color
        special_flag: int = move.get_special_flag()
        piece: int = move.get_moving_piece()

        if special_flag == SpecialFlags.CASTLING.value:
            score += 50

        if target_square in BoardEnum.CENTER_MAIN_SQUARES.value:
            score += 2 * EvalEnum.MAIN_CENTER.value
        if target_square in BoardEnum.CENTER_SIDE_SQUARES.value:
            score += EvalEnum.SIDE_CENTER.value

        if special_flag in SpecialFlags.PROMOTIONS.value:
            color: int = PiecesEnum.WHITE.value
            piece_value: int = BoardUtil.get_promotion_piece(color, special_flag) - color

            score += StaticEvalUtil.get_piece_point_value(piece_value)

        if piece in (PiecesEnum.KNIGHT.value, PiecesEnum.BISHOP.value):
            score += StaticEvalUtil.get_piece_point_value(piece)

        if target_piece != 0:
            target_eval: int = StaticEvalUtil.get_piece_point_value(target_piece_value)
            friendly_eval: int = StaticEvalUtil.get_piece_point_value(piece)

            score += 3 * target_eval - friendly_eval
        return score
