from typing import Optional
from typing import TYPE_CHECKING

from numpy import array
from numpy import dtype
from numpy import int8
from numpy import ndarray

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move

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
        if None in (move, board):
            raise NullArgumentException("CANNOT WORK WITH NULLS!")

        if move.get_moving_piece() != PiecesEnum.PAWN.value or board.en_passant_square() == -1:
            return False
        if board.en_passant_piece_square() == -1:
            return False

        return move.get_end_square() == board.en_passant_square()

    @staticmethod
    def get_attack_direction(color: int, direction: str, engine_color: int) -> int:
        """
        Gets proper int direction of end_square
        :param engine_color: color of upper pieces
        :param color: int value of color
        :param direction: str attack direction
        :return: int
        """
        if None in (color, direction, engine_color):
            raise NullArgumentException("I CANNOT WORK ON NULLS!")
        if not ColorManager.is_it_valid_color(color) or not ColorManager.is_it_valid_color(engine_color):
            raise IllegalArgumentException("INVALID COLOR VALUES!")
        if direction not in ("LEFT", "RIGHT"):
            raise IllegalArgumentException("IMPOSSIBLE DIRECTION!")

        player_color: int = ColorManager.get_opposite_piece_color(engine_color)
        direct: str = direction.upper()
        pawn_direction_dict = {
            ("LEFT", player_color): MoveEnum.PAWN_UP_LEFT_ATTACK.value,
            ("RIGHT", player_color): MoveEnum.PAWN_UP_RIGHT_ATTACK.value,
            ("LEFT", engine_color): MoveEnum.PAWN_DOWN_LEFT_ATTACK.value,
            ("RIGHT", engine_color): MoveEnum.PAWN_DOWN_RIGHT_ATTACK.value
        }
        return pawn_direction_dict[direct, color]

    @staticmethod
    def is_pawn_promoting(move: Move, color: int, engine_color: int) -> bool:
        """
        Methods checks if pawn is promoting or not
        :param engine_color: color of upper pieces
        :param move: Move instance
        :param color: int value of color
        :return: bool
        """
        if None in (move, color, engine_color):
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if not ColorManager.is_it_valid_color(color) or not ColorManager.is_it_valid_color(engine_color):
            raise IllegalArgumentException("SUCH COLORS DOES NOT EXIST!")
        end_square: Optional[int] = move.get_end_square()

        if end_square is None:
            raise NullArgumentException("END SQUARE CANNOT BE NULL!")

        if move.get_moving_piece() != PiecesEnum.PAWN.value:
            return False
        if engine_color and 0 <= end_square <= 7:
            return True
        player_color: int = ColorManager.get_opposite_piece_color(engine_color)

        return color == player_color and 57 <= end_square <= 63

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
        if None in (double_move_target, start_square, board, step):
            raise NullArgumentException("CANNOT WORK ON NULLS!")
        if double_move_target < 0 or double_move_target > 63 or start_square < 0 or start_square > 63:
            raise IllegalArgumentException("SQUARES OUT OF BOARD BOUNDS!")
        piece_single_up: int = board.board_array()[start_square + step]
        piece_double_up: int = board.board_array()[double_move_target]

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
        if None in (start_square, move_target, attack_range):
            raise NullArgumentException("DO NOT PASS NULLS AS ARGUMENTS!")
        if start_square < 0 or start_square > 63 or move_target < 0 or move_target > 63:
            raise IllegalArgumentException("SQUARES OUT OF BOARD BOUNDS!")

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
        if special_flag is None:
            raise NullArgumentException("SPECIAL FLAG SHOULD NOT BE NULL!")

        promotions: ndarray[int, dtype[int8]] = array([SpecialFlags.PROMOTE_TO_ROOK.value,
                                                       SpecialFlags.PROMOTE_TO_QUEEN.value,
                                                       SpecialFlags.PROMOTE_TO_BISHOP.value,
                                                       SpecialFlags.PROMOTE_TO_KNIGHT.value], dtype=int8)
        return special_flag in promotions
