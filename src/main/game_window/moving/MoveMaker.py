from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenUtil import FenUtil
from game_window.ColorManager import ColorManager
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveMakingUtil import MoveMakingUtil
from game_window.moving.MoveUnMakingUtil import MoveUnMakingUtil

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveMaker:
    """
    Class containing methods to make and unmake __moves
    """

    __slots__ = ()

    @staticmethod
    def make_move(move: Move, color: int, board: 'Board') -> MoveData:
        """
        Method used to make a given move. It means to update the board int array
        :param board: Board instance
        :param move: Move instance - move we want to make
        :param color: color of a piece
        :return: MoveData instance containing fen_data before the move and the deleted piece by move
        """
        fen_data: FenData = board.get_fen_data()
        end_square: int = move.get_end_square()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        move_data: MoveData = MoveMakingUtil.copy_fen_data_to_move_data(board)
        enemy_color: int = ColorManager.get_opposite_piece_color(color)

        if board_array[end_square] == enemy_color | PiecesEnum.ROOK.value:
            FenUtil.disable_castling_on_side(enemy_color, end_square, board)
        FenUtil.update_fen_data_with_double_pawn_movement(move, fen_data)

        if MoveMakingUtil.check_and_handle_rook_movement(move, board, color, move_data):
            return move_data
        if MoveMakingUtil.check_and_handle_promotion_movement(move, board, color, move_data):
            return move_data
        if MoveMakingUtil.check_and_handle_castling_movement(move, board, color, move_data):
            return move_data
        if MoveMakingUtil.check_and_handle_en_passant_movement(move, board, color, move_data):
            return move_data
        if MoveMakingUtil.check_and_handle_kings_movement(move, board, color, move_data):
            return move_data
        MoveMakingUtil.update_move_data_with_deleted_piece(move_data, board, color, move)

        return move_data

    @staticmethod
    def un_make_move(move: Move, deleted_data: MoveData, board: 'Board') -> None:
        """
        Removes given move with a value of deleted piece
        :param deleted_data: MoveData instance
        :param board: Board instance
        :param move: move to be unmade
        :return: None
        """
        deleted_piece: int = deleted_data.deleted_piece
        color: int = ColorManager.get_piece_color(deleted_piece)

        if MoveUnMakingUtil.check_and_un_make_castling_move(move, deleted_data, board, color):
            return
        if MoveUnMakingUtil.check_and_un_make_promotion_move(move, deleted_data, board):
            return
        if MoveUnMakingUtil.check_and_un_make_en_passant_move(move, deleted_data, board):
            return
        MoveUnMakingUtil.un_make_basic_move(move, deleted_data, board)
