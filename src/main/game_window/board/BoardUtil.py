from typing import TYPE_CHECKING

from numpy import int8
from numpy import ndarray
from numpy import zeros

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.exceptions.NullArgumentException import NullArgumentException

if TYPE_CHECKING:
    from game_window.board.Board import Board


class BoardUtil:
    """
    Util class for Board class
    """

    __slots__ = ()

    @staticmethod
    def calculate_distance_to_borders() -> ndarray[int]:
        """
        Calculates array of distances of each end_square in every direction to board borders.
        :return: ndarray of distances
        """
        distances = zeros((BoardEnum.BOARD_SIZE.value, BoardEnum.BOARD_LENGTH.value), dtype=int8)

        for row in range(BoardEnum.BOARD_LENGTH.value):
            for col in range(BoardEnum.BOARD_LENGTH.value):
                squares_to_top = row
                squares_to_bottom = 7 - row
                square_to_left = col
                squares_to_right = 7 - col
                squares_to_top_left = min(squares_to_top, square_to_left)
                squares_to_top_right = min(squares_to_top, squares_to_right)
                squares_to_bottom_right = min(squares_to_bottom, squares_to_right)
                squares_to_bottom_left = min(squares_to_bottom, square_to_left)
                square_index = 8 * row + col

                distances[square_index] = [
                    squares_to_top_left,
                    squares_to_top,
                    squares_to_top_right,
                    square_to_left,
                    squares_to_right,
                    squares_to_bottom_left,
                    squares_to_bottom,
                    squares_to_bottom_right
                ]
        return distances

    @staticmethod
    def is_board_inverted(board: 'Board') -> bool:
        """
        Method used to check if board is not inverted.
        :param board: Board instance
        :return: bool
        """
        if board is None:
            raise NullArgumentException("BOARD CANNOT BE NULL!")
        return board.get_engine_color() == PiecesEnum.WHITE.value

