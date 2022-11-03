from typing import Dict

from numpy import int8, dtype
from numpy import ndarray
from numpy import zeros
from typing import TYPE_CHECKING

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags

if TYPE_CHECKING:
    from game_window.board.Board import Board


class BoardUtil:
    """
    Util class for Board class
    """

    __slots__ = ()

    @staticmethod
    def calculate_distance_to_borders() -> ndarray[int, dtype[int8]]:
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

    @staticmethod
    def get_promotion_piece(color: int, flag: int) -> int:
        """
        Method used to return a promotion piece depending on a flag
        :param color: int value of piece color
        :param flag: int value of promotion flag
        :return: int value of piece
        """
        if color is None or flag is None:
            raise NullArgumentException("COLOR AND FLAG CANNOT BE NULLS!")
        if not ColorManager.is_it_valid_color(color) or flag not in SpecialFlags.PROMOTIONS.value:
            raise IllegalArgumentException("COLOR OR FLAG HAS NOT PROPER VALUES!")

        promotion_pieces: Dict[int, int] = {
            SpecialFlags.PROMOTE_TO_QUEEN.value: PiecesEnum.QUEEN.value,
            SpecialFlags.PROMOTE_TO_KNIGHT.value: PiecesEnum.KNIGHT.value,
            SpecialFlags.PROMOTE_TO_ROOK.value: PiecesEnum.ROOK.value,
            SpecialFlags.PROMOTE_TO_BISHOP.value: PiecesEnum.BISHOP.value
        }
        return color | promotion_pieces[flag]
