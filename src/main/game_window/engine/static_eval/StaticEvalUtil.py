from typing import TYPE_CHECKING

from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SquaresEval import SquaresEval

if TYPE_CHECKING:
    from game_window.board.Board import Board


class StaticEvalUtil:
    """
    Utility class for static eval methods
    """

    __slots__ = ()

    @staticmethod
    def return_proper_evaluation_signed_value(board: 'Board', evaluation: float, favor_color: int) -> float:
        """
        Method used to return a proper mark of evaluation based on favor_color to move
        :param favor_color:
        :param board: Board instance
        :param evaluation: int value of evaluation
        :return: int value with proper sign
        """
        return evaluation if favor_color == board.engine_color() else -evaluation

    @staticmethod
    def is_queen_on_start_position(color: int, board: 'Board') -> bool:
        """
        Method used to check if queen is on starting position
        :param color: int vale of color
        :param board: Board instance
        :return: bool
        """
        start_positions = {
            board.engine_color(): 3,
            board.player_color(): 59
        }

        for square, piece in enumerate(board.board_array()):
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

    @staticmethod
    def get_pieces_square_points(piece_value: int, pieces_color: int, square: int, board: 'Board') -> float:
        """

        :param board:
        :param square:
        :param piece_value:
        :param pieces_color:
        :return:
        """
        engine_color: int = board.engine_color()
        player_color: int = board.player_color()

        if piece_value == PiecesEnum.QUEEN.value:
            return SquaresEval.QUEEN.value[square]
        if piece_value == PiecesEnum.KNIGHT.value:
            return SquaresEval.KNIGHT.value[square]

        squares_dict = {
            (engine_color, PiecesEnum.KING.value): SquaresEval.ENGINE_KING.value[square],
            (engine_color, PiecesEnum.ROOK.value): SquaresEval.ENGINE_ROOK.value[square],
            (engine_color, PiecesEnum.PAWN.value): SquaresEval.ENGINE_PAWN.value[square],
            (engine_color, PiecesEnum.BISHOP.value): SquaresEval.ENGINE_BISHOP.value[square],
            (player_color, PiecesEnum.KING.value): SquaresEval.PLAYER_KING.value[square],
            (player_color, PiecesEnum.ROOK.value): SquaresEval.PLAYER_ROOK.value[square],
            (player_color, PiecesEnum.PAWN.value): SquaresEval.PLAYER_PAWN.value[square],
            (player_color, PiecesEnum.BISHOP.value): SquaresEval.PLAYER_BISHOP.value[square]
        }
        return squares_dict[pieces_color, piece_value]
