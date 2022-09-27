from numpy import array
from numpy import ndarray

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move


class CheckUtil:
    @staticmethod
    def find_friendly_king_squares(board_array: ndarray[int], color_to_move: int) -> int:
        for index in range(BoardEnum.BOARD_SIZE.value):
            if board_array[index] == color_to_move | PiecesEnum.KING.value:
                return index
        return -1

    @staticmethod
    def get_castling_squares(move: Move):
        move_distance = move.get_end_square() - move.get_start_square()

        if move_distance > 0:
            return array([move.get_start_square(), move.get_start_square() + 1, move.get_start_square() + 2])
        return array([move.get_start_square(), move.get_start_square() - 1, move.get_start_square() - 2])
