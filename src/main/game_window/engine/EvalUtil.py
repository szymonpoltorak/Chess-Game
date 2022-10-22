from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_window.Board import Board


class EvalUtil:
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
