from typing import TYPE_CHECKING

from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class StaticEvalUtil:
    """
    Utility class for static eval methods
    """

    __slots__ = ()

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
    def is_queen_on_start_position(color: int, board: 'Board') -> bool:
        """
        Method used to check if queen is on starting position
        :param color: int vale of color
        :param board: Board instance
        :return: bool
        """
        start_positions = {
            board.get_engine_color(): 3,
            board.get_player_color(): 59
        }

        for square, piece in enumerate(board.get_board_array()):
            if piece == color | PiecesEnum.QUEEN.value and start_positions[color] == square:
                return True
        return False

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
