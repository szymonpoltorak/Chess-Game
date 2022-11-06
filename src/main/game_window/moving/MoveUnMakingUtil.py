from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.board.fen.FenData import FenData
from game_window.ColorManager import ColorManager
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveUnMakingUtil:
    """
    Utility class for un making moves
    """

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
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()

        if special_flag == SpecialFlags.CASTLING.value:
            board.un_castle_king(move, color)
            fen_data.update_fen_data(deleted_data)
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
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()

        if special_flag in SpecialFlags.PROMOTIONS.value:
            fen_data.update_fen_data(deleted_data)
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
        fen_data: FenData = board.get_fen_data()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        special_flag: int = move.get_special_flag_value()
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()

        if special_flag == SpecialFlags.EN_PASSANT.value:
            fen_data.update_fen_data(deleted_data)
            moved_piece: int = board_array[end_square]
            friendly_color: int = ColorManager.get_piece_color(moved_piece)
            enemy_color: int = ColorManager.get_opposite_piece_color(friendly_color)

            board_array[fen_data.get_en_passant_square()] = 0
            board_array[fen_data.get_en_passant_piece_square()] = enemy_color | PiecesEnum.PAWN.value
            board_array[start_square] = moved_piece
            return True
        return False

    @staticmethod
    def un_make_basic_move(move: Move, deleted_data: MoveData, board: 'Board') -> None:
        """
        Method used to un make not special moves
        :param move: Move instance
        :param deleted_data: MoveData instance
        :param board: Board instance
        :return: None
        """
        fen_data: FenData = board.get_fen_data()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()

        fen_data.update_fen_data(deleted_data)
        moved_piece: int = board_array[end_square]
        board_array[end_square] = deleted_data.deleted_piece
        board_array[start_square] = moved_piece
