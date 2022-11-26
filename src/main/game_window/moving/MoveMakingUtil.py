from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray
from numpy import sign

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.BoardUtil import BoardUtil
from game_window.ColorManager import ColorManager
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveData import MoveData
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveMakingUtil:
    """
    Utility class for making __moves
    """

    @staticmethod
    def castle_king(piece: int, move: Move, board: 'Board') -> None:
        """
        Method used to castle king it means prepare board for castling
        :param piece: int value of piece_square
        :param move: Move instance
        :param board: Board instance
        :return: None
        """
        if None in (piece, move, board):
            raise NullArgumentException("METHODS ARGUMENTS CANNOT BE NULLS!")
        color: int = ColorManager.get_piece_color(piece)
        piece_value = piece - color

        if piece_value != PiecesEnum.KING.value:
            raise IllegalArgumentException("YOU CANNOT CASTLE PIECE WHICH IS NOT KING!")
        if move.get_special_flag() != SpecialFlags.CASTLING.value:
            raise IllegalArgumentException("THIS IS NOT CASTLING MOVE!")

        start_square: int = move.get_start_square()
        board_array: ndarray[int, dtype[int8]] = board.board_array()
        end_square: int = move.get_end_square()
        distance: int = start_square - end_square
        is_queen_side: bool = distance > 0
        rook_position: int = KingUtil.get_rook_position(color, is_queen_side, board.engine_color(), board.player_color())

        board_array[start_square] = PiecesEnum.NONE.value
        board_array[end_square] = piece
        board_array[rook_position] = PiecesEnum.NONE.value
        board_array[end_square + sign(distance)] = color | PiecesEnum.ROOK.value

        board.set_castling_king_side(False, color)
        board.set_castling_queen_side(False, color)

    @staticmethod
    def make_en_passant_capture(piece: int, board: 'Board') -> None:
        """
        Method used to make an en passant capture on board array
        :param piece: int value of piece
        :param board: Board instance
        :return: None
        """
        piece_value: int = piece - ColorManager.get_piece_color(piece)
        board_array: ndarray[int, dtype[int8]] = board.board_array()

        if piece_value != PiecesEnum.PAWN.value:
            raise IllegalArgumentException("THIS PIECE CANNOT MAKE AN EN PASSANT CAPTURE!")
        if piece is None:
            raise NullArgumentException("PIECE CANNOT BE NULL!")

        board_array[board.en_passant_square()] = piece
        board_array[board.en_passant_piece_square()] = 0

        board.set_en_passant_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
        board.set_en_passant_piece_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)

        board.update_fen()

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
            board.disable_castling_on_side(board.engine_color(), move.get_start_square())
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
        board_array: ndarray[int, dtype[int8]] = board.board_array()
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
            MoveMakingUtil.castle_king(deleted_piece, move, board)
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

            MoveMakingUtil.make_en_passant_capture(move_data.deleted_piece, board)
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

        if moving_piece == PiecesEnum.KING.value:
            MoveMakingUtil.update_move_data_with_deleted_piece(move_data, board, color, move)
            board.set_castling_king_side(False, board.engine_color())
            board.set_castling_queen_side(False, board.engine_color())
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
        board_array: ndarray[int, dtype[int8]] = board.board_array()
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
        Method used to copy fen data for making __moves
        :param board: Board instance
        :return: MoveData instance without deleted piece value
        """
        return MoveData(MoveEnum.NONE.value, *board.get_special_move_data())
