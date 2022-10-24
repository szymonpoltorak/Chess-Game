from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.board.fen.FenData import FenData
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move

if TYPE_CHECKING:
    from game_window.board.Board import Board


class PawnUtil:
    """
    Util class containing methods helping with pawn evaluation
    """

    __slots__ = ()

    @staticmethod
    def was_it_en_passant_move(move: Move, board: 'Board') -> bool:
        """
        Methods checks if it was an en passant move
        :param move: Move instance
        :param board: Board instance
        :return: bool
        """
        fen_data: FenData = board.get_fen_data()

        if move.get_moving_piece() != PiecesEnum.PAWN.value or fen_data.get_en_passant_square() == -1:
            return False
        if fen_data.get_en_passant_piece_square() == -1:
            return False

        return move.get_end_square() == fen_data.get_en_passant_square()

    @staticmethod
    def get_attack_direction(color: int, direction: str, upper_color: int) -> int:
        """
        Gets proper int direction of end_square
        :param upper_color: color of upper pieces
        :param color: int value of color
        :param direction: str attack direction
        :return: int
        """
        down_color: int = ColorManager.get_opposite_piece_color(upper_color)
        direct: str = direction.upper()
        pawn_direction_dict = {
            ("LEFT", down_color): MoveEnum.PAWN_UP_LEFT_ATTACK.value,
            ("RIGHT", down_color): MoveEnum.PAWN_UP_RIGHT_ATTACK.value,
            ("LEFT", upper_color): MoveEnum.PAWN_DOWN_LEFT_ATTACK.value,
            ("RIGHT", upper_color): MoveEnum.PAWN_DOWN_RIGHT_ATTACK.value
        }
        return pawn_direction_dict[direct, color]

    @staticmethod
    def is_pawn_promoting(move: Move, color: int, upper_color: int) -> bool:
        """
        Methods checks if pawn is promoting or not
        :param upper_color: color of upper pieces
        :param move: Move instance
        :param color: int value of color
        :return: bool
        """
        if move.get_moving_piece() != PiecesEnum.PAWN.value:
            return False
        if upper_color and 0 <= move.get_end_square() <= 7:
            return True
        opposite_color: int = ColorManager.get_opposite_piece_color(upper_color)

        return color == opposite_color and 57 <= move.get_end_square() <= 63

    @staticmethod
    def no_piece_in_pawns_way(double_move_target: int, start_square: int, board: 'Board', step: int) -> bool:
        """
        Static method used to check if there is any piece_square on pawns way
        :param double_move_target: int target end_square of pawns double move
        :param start_square: int index of starting end_square
        :param board: Board instance
        :param step: int value of step
        :return: bool
        """
        piece_single_up: int = board.get_board_array()[start_square + step]
        piece_double_up: int = board.get_board_array()[double_move_target]

        return piece_double_up == 0 and piece_single_up == 0

    @staticmethod
    def is_attack_target_in_border_bounds(start_square: int, move_target: int, attack_range: int) -> bool:
        """
        Static method to check if pawns attack target is in board bonds
        :param start_square: int index of start end_square
        :param move_target: int index of attack target end_square
        :param attack_range: int value of range attack
        :return: bool
        """
        start_col: int = start_square % BoardEnum.BOARD_LENGTH.value
        target_col: int = move_target % BoardEnum.BOARD_LENGTH.value

        return abs(start_col - target_col) <= attack_range

    @staticmethod
    def is_it_a_promotion(special_flag: int) -> bool:
        """
        Checks if it is a promotion
        :param special_flag: int value of a special flag
        :return: bool
        """
        promotions: ndarray[int] = array([SpecialFlags.PROMOTE_TO_ROOK.value, SpecialFlags.PROMOTE_TO_QUEEN.value,
                                          SpecialFlags.PROMOTE_TO_BISHOP.value, SpecialFlags.PROMOTE_TO_KNIGHT.value])
        return special_flag in promotions
