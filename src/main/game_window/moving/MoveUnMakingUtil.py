from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray
from numpy import sign

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveData import MoveData

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveUnMakingUtil:
    """
    Utility class for un making __moves
    """

    @staticmethod
    def un_castle_king(move: Move, color: int, board: 'Board') -> None:
        """
        Method used to un castle king of given color
        :param move: Move which king made
        :param color: color value of a king
        :param board: Board instance
        :return: None
        """
        if move is None or color is None:
            raise NullArgumentException("MOVE AND COLOR CANNOT BE NULLS!")
        if move.get_special_flag() != SpecialFlags.CASTLING.value:
            raise IllegalArgumentException("IT IS NOT CASTLING MOVE!")
        if color not in (PiecesEnum.WHITE.value, PiecesEnum.BLACK.value):
            raise IllegalArgumentException("SUCH COLOR NOT EXISTS!")

        board_array: ndarray[int, dtype[int8]] = board.board_array()
        start_square: int = move.get_start_square()
        end_square: int = move.get_end_square()
        distance: int = start_square - end_square
        is_queen_side: bool = distance > 0
        rook_position: int = KingUtil.get_rook_position(color, is_queen_side, board.engine_color(), board.player_color())

        board_array[rook_position] = color | PiecesEnum.ROOK.value
        board_array[move.get_end_square()] = PiecesEnum.NONE.value
        board_array[end_square + sign(distance)] = PiecesEnum.NONE.value
        board_array[move.get_start_square()] = color | PiecesEnum.KING.value

    @staticmethod
    def check_and_un_make_castling_move(move: Move, deleted_data: MoveData, board: 'Board', color: int) -> bool:
        """
        Method used to check if it is castling move and if so un make it
        :param move: Move instance
        :param deleted_data: MoveData instance
        :param board: Board instance
        :param color: int value of color
        :return: bool
        """
        special_flag: int = move.get_special_flag()

        if special_flag == SpecialFlags.CASTLING.value:
            MoveUnMakingUtil.un_castle_king(move, color, board)
            board.update_fen_data(deleted_data)
            return True
        return False

    @staticmethod
    def check_and_un_make_promotion_move(move: Move, deleted_data: MoveData, board: 'Board') -> bool:
        """
        Method used to check if it is promotion move and if so un make it
        :param move: Move instance
        :param deleted_data: MoveData instance
        :param board: Board instance
        :return: bool
        """
        special_flag: int = move.get_special_flag()
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()

        if special_flag in SpecialFlags.PROMOTIONS.value:
            board.update_fen_data(deleted_data)
            color = ColorManager.get_piece_color(board_array[end_square])

            moved_piece = color | move.get_moving_piece()
            board_array[end_square] = deleted_data.deleted_piece
            board_array[start_square] = moved_piece
            return True
        return False

    @staticmethod
    def check_and_un_make_en_passant_move(move: Move, deleted_data: MoveData, board: 'Board') -> bool:
        """
        Method used to check if it is en passant move and if so un make it
        :param move: Move instance
        :param deleted_data: MoveData instance
        :param board: Board instance
        :return: bool
        """
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        special_flag: int = move.get_special_flag()
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()

        if special_flag == SpecialFlags.EN_PASSANT.value:
            board.update_fen_data(deleted_data)
            moved_piece: int = board_array[end_square]
            friendly_color: int = ColorManager.get_piece_color(moved_piece)
            enemy_color: int = ColorManager.get_opposite_piece_color(friendly_color)

            board_array[board.en_passant_square()] = 0
            board_array[board.en_passant_piece_square()] = enemy_color | PiecesEnum.PAWN.value
            board_array[start_square] = moved_piece
            return True
        return False

    @staticmethod
    def un_make_basic_move(move: Move, deleted_data: MoveData, board: 'Board') -> None:
        """
        Method used to un make not special __moves
        :param move: Move instance
        :param deleted_data: MoveData instance
        :param board: Board instance
        :return: None
        """
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()

        board.update_fen_data(deleted_data)
        moved_piece: int = board_array[end_square]
        board_array[end_square] = deleted_data.deleted_piece
        board_array[start_square] = moved_piece
