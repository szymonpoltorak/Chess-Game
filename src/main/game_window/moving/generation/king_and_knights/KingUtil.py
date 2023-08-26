from typing import TYPE_CHECKING

from numpy._typing import NDArray

from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.ColorManager import ColorManager
from src.main.game_window.board.BoardUtil import BoardUtil
from src.main.game_window.enums.BoardEnum import BoardEnum
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.moving.generation.data.Move import Move
from numpy import array
from numpy import dtype
from numpy import int8

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class KingUtil:
    """
    Class containing util methods for king and knight __moves creation
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
        if board is None or start_square is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if start_square < 0 or start_square > 63:
            raise IllegalArgumentException("START SQUARE IS OUT OF BONDS!")

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
        if board is None or start_square is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if start_square < 0 or start_square > 63:
            raise IllegalArgumentException("START SQUARE IS OUT OF BONDS!")

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
        if None in (board, step, side_value, start_square):
            raise NullArgumentException("YOU CANNOT PASS NULLS AS ARGUMENTS!")
        if start_square < 0 or start_square > 63:
            raise IllegalArgumentException("START SQUARE IS OUT OF BONDS!")

        for i in range(1, side_value + 1):
            index: int = start_square + step * i

            if index > 63 or index < 0:
                break
            if board.board_array()[start_square + step * i] != 0:
                return True
        return False

    @staticmethod
    def is_it_castling(move: Move) -> bool:
        """
        Checks if this move is castling
        :param move: Move instance
        :return: bool
        """
        if move is None:
            raise NullArgumentException("MOVE CANNOT BE NULL!")
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()
        moving_piece: int = move.get_moving_piece()

        move_length: int = abs(end_square - start_square)

        return moving_piece == PiecesEnum.KING.value and move_length == MoveEnum.CASTLE_MOVE.value

    @staticmethod
    def get_rook_position(color: int, is_queen_side: bool, engine_color: int, player_color: int) -> int:
        """
        Static method to return rooks board position based on given parameters
        :param player_color: value of down pieces color
        :param engine_color: value of upper pieces color
        :param color: rook color
        :param is_queen_side: bool
        :return: int value of rook position
        """
        if None in (color, is_queen_side, engine_color, player_color):
            raise NullArgumentException("I CANNOT WORK WITH NULL ARGUMENTS!")
        if not ColorManager.is_it_valid_color(color) or not ColorManager.is_it_valid_color(engine_color) or \
                not ColorManager.is_it_valid_color(player_color):
            raise IllegalArgumentException("COLORS HAVE NOT PROPER VALUES!")

        move_dict = {
            (True, player_color): MoveEnum.BOTTOM_ROOK_QUEEN.value,
            (True, engine_color): MoveEnum.TOP_ROOK_QUEEN.value,
            (False, player_color): MoveEnum.BOTTOM_ROOK_KING.value,
            (False, engine_color): MoveEnum.TOP_ROOK_KING.value
        }
        return move_dict[is_queen_side, color]

    @staticmethod
    def get_castling_squares(move: Move) -> NDArray[int]:
        """
        Method used to get castling squares depending on given move
        :param move: Move instance
        :return: NDArray of ints 1D
        """
        if move is None:
            raise NullArgumentException("MOVE CANNOT BE NULL!")

        end_square: int = move.get_end_square()
        start_square: int = move.get_end_square()
        move_distance: int = end_square - start_square

        if move_distance > 0:
            return array([start_square, start_square + 1, start_square + 2])
        return array([start_square, start_square - 1, start_square - 2])

    @staticmethod
    def find_friendly_king_squares(board_array: NDArray[int], color_to_move: int) -> int:
        """
        Finds a friendly king on given board array
        :param board_array: ndarray of board 1D
        :param color_to_move:
        :return: int value of index
        """
        if board_array is None or color_to_move is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if not ColorManager.is_it_valid_color(color_to_move):
            raise IllegalArgumentException("COLOR DOES NOT EXISTS!")

        for index in range(BoardEnum.BOARD_SIZE.value):
            if board_array[index] == color_to_move | PiecesEnum.KING.value:
                return index
        raise ValueError("THERE IS NO FRIENDLY KING AND IT IS NOT POSSIBLE!")
