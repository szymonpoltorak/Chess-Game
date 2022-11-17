from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.board.BoardUtil import BoardUtil
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenUtil import FenUtil
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveMakingUtil:
    """
    Utility class for making moves
    """

    @staticmethod
    def check_and_handle_rook_movement(move: Move, board: 'Board', color: int, move_data: MoveData) -> bool:
        """
        Method used to check if moving piece is rook and if so handle its movement
        :param move: Move instance
        :param board: Board instance
        :param color: int value of color
        :param move_data: MoveData instance
        :return: None
        """
        moving_piece: int = move.get_moving_piece()

        if moving_piece == PiecesEnum.ROOK.value:
            MoveMakingUtil.update_move_data_with_deleted_piece(move_data, board, color, move)
            FenUtil.disable_castling_on_side(board.get_engine_color(), move.get_start_square(), board)
            return True
        return False

    @staticmethod
    def check_and_handle_promotion_movement(move: Move, board: 'Board', color: int, move_data: MoveData) -> bool:
        """
        Method used to check if it is promotion move and if so handle its movement
        :param move: Move instance
        :param board: Board instance
        :param color: int value of color
        :param move_data: MoveData instance
        :return: bool
        """
        special_flag: int = move.get_special_flag()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        end_square: int = move.get_end_square()

        if special_flag in SpecialFlags.PROMOTIONS.value:
            MoveMakingUtil.update_move_data_with_deleted_piece(move_data, board, color, move)
            board_array[end_square] = BoardUtil.get_promotion_piece(color, special_flag)
            return True
        return False

    @staticmethod
    def check_and_handle_castling_movement(move: Move, board: 'Board', color: int, move_data: MoveData) -> bool:
        """
        Method used to check if it is castling move and if so handle its movement
        :param move: Move instance
        :param board: Board instance
        :param color: int value of color
        :param move_data: MoveData instance
        :return: bool
        """
        special_flag: int = move.get_special_flag()
        moving_piece: int = move.get_moving_piece()

        if special_flag == SpecialFlags.CASTLING.value:
            deleted_piece = color | moving_piece
            move_data.deleted_piece = deleted_piece
            board.castle_king(deleted_piece, move)
            return True
        return False

    @staticmethod
    def check_and_handle_en_passant_movement(move: Move, board: 'Board', color: int, move_data: MoveData) -> bool:
        """
        Method used to check if it is en passant move and if so handle its movement
        :param move: Move instance
        :param board: Board instance
        :param color: int value of color
        :param move_data: MoveData instance
        :return: bool
        """
        special_flag: int = move.get_special_flag()

        if special_flag == SpecialFlags.EN_PASSANT.value:
            move_data.deleted_piece = board.delete_piece_from_board_square(move.get_start_square())

            board.make_en_passant_capture(move_data.deleted_piece)
            return True
        return False

    @staticmethod
    def check_and_handle_kings_movement(move: Move, board: 'Board', color: int, move_data: MoveData) -> bool:
        """
        Method used to check if moving piece is king and if so handle its movement
        :param move: Move instance
        :param board: Board instance
        :param color: int value of color
        :param move_data: MoveData instance
        :return: bool
        """
        moving_piece: int = move.get_moving_piece()
        fen_data: FenData = board.get_fen_data()

        if moving_piece == PiecesEnum.KING.value:
            MoveMakingUtil.update_move_data_with_deleted_piece(move_data, board, color, move)
            fen_data.set_castling_king_side(False, board.get_engine_color())
            fen_data.set_castling_queen_side(False, board.get_engine_color())
            return True
        return False

    @staticmethod
    def update_board_with_movement(board: 'Board', move: Move, color: int) -> int:
        """
        Method used update board with movement and return the piece on movement end square
        :param board: Board instance
        :param move: Move instance
        :param color: int value of color
        :return: int value of deleted piece by move
        """
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        end_square: int = move.get_end_square()

        deleted_piece: int = board_array[end_square]
        board_array[move.get_start_square()] = 0
        board_array[end_square] = color | move.get_moving_piece()

        return deleted_piece

    @staticmethod
    def update_move_data_with_deleted_piece(move_data: MoveData, board: 'Board', color: int, move: Move) -> None:
        """
        Method used update move data with deleted piece value
        :param move_data: MoveData instance
        :param board: Board instance
        :param color: int value of color
        :param move: Move instance
        :return: None
        """
        move_data.deleted_piece = MoveMakingUtil.update_board_with_movement(board, move, color)

    @staticmethod
    def copy_fen_data_to_move_data(board: 'Board') -> MoveData:
        """
        Method used to copy fen data for making moves
        :param board: Board instance
        :return: MoveData instance without deleted piece value
        """
        fen_data: FenData = board.get_fen_data()

        return MoveData(MoveEnum.NONE.value, *fen_data.get_special_move_data())
