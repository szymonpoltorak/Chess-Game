from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.board.BoardUtil import BoardUtil
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.Move import Move

if TYPE_CHECKING:
    from game_window.board.Board import Board


class KingUtil:
    """
    Class containing util methods for king and knight moves creation
    """

    __slots__ = ()
    
    @staticmethod
    def is_anything_on_king_side(board: 'Board', start_square: int) -> bool:
        """
        Checks if there is anything on the path between a king side rook and the king
        :param board: Board instance
        :param start_square: int index of kings end_square
        :return: bool
        """
        step = -1 if BoardUtil.is_board_inverted(board) else 1

        return KingUtil.check_castling_squares(step, MoveEnum.KING_SIDE.value, start_square, board)

    @staticmethod
    def is_anything_on_queen_side(board: 'Board', start_square: int) -> bool:
        """
        Checks if there is anything on the path between a queen side rook and the king
        :param board: Board instance
        :param start_square: int index of kings end_square
        :return: bool
        """
        step = 1 if BoardUtil.is_board_inverted(board) else -1

        return KingUtil.check_castling_squares(step, MoveEnum.QUEEN_SIDE.value, start_square, board)

    @staticmethod
    def check_castling_squares(step: int, side_value: int, start_square: int, board: 'Board') -> bool:
        """
        Checks if there is something on castling squares.
        :param step: step of direction
        :param side_value: value of King or Queen side
        :param start_square: start square of move
        :param board: Board instance
        :return: bool
        """
        for i in range(1, side_value + 1):
            index: int = start_square + step * i

            if index > 63 or index < 0:
                break
            if board.get_board_array()[start_square + step * i] != 0:
                return True
        return False

    @staticmethod
    def is_it_castling(move: Move) -> bool:
        """
        Checks if this move is castling
        :param move: Move instance
        :return: bool
        """
        move_length: int = abs(move.get_end_square() - move.get_start_square())

        return move.get_moving_piece() == PiecesEnum.KING.value and move_length == MoveEnum.CASTLE_MOVE.value

    @staticmethod
    def get_rook_position(color: int, is_queen_side: bool, upper_color: int, down_color: int) -> int:
        """
        Static method to return rooks board position based on given parameters
        :param down_color: value of down pieces color
        :param upper_color: value of upper pieces color
        :param color: rook color
        :param is_queen_side: bool
        :return: int value of rook position
        """
        move_dict = {
            (True, down_color): MoveEnum.BOTTOM_ROOK_QUEEN.value,
            (True, upper_color): MoveEnum.TOP_ROOK_QUEEN.value,
            (False, down_color): MoveEnum.BOTTOM_ROOK_KING.value,
            (False, upper_color): MoveEnum.TOP_ROOK_KING.value
        }
        return move_dict[is_queen_side, color]

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