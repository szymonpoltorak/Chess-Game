from numpy import array
from numpy import ndarray

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.Move import Move


class CheckUtil:
    __slots__ = ()

    @staticmethod
    def find_friendly_king_squares(board_array: ndarray[int], color_to_move: int) -> int:
        """
        Finds a friendly king on given board array
        :param board_array: ndarray of board 1D
        :param color_to_move:
        :return: int value of index
        """
        for index in range(BoardEnum.BOARD_SIZE.value):
            if board_array[index] == color_to_move | PiecesEnum.KING.value:
                return index
        raise ValueError("THERE IS NO FRIENDLY KING AND IT IS NOT POSSIBLE!")

    @staticmethod
    def get_castling_squares(move: Move) -> ndarray[int]:
        """
        Method used to get castling squares depending on given move
        :param move: Move instance
        :return: ndarray of ints 1D
        """
        end_square: int = move.get_end_square()
        start_square: int = move.get_end_square()
        move_distance: int = end_square - start_square

        if move_distance > 0:
            return array([start_square, start_square + 1, start_square + 2])
        return array([start_square, start_square - 1, start_square - 2])
