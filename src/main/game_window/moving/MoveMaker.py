from numpy import ndarray, int8, dtype
from typing import TYPE_CHECKING

from game_window.board.BoardUtil import BoardUtil
from game_window.ColorManager import ColorManager
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenUtil import FenUtil
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveMaker:
    """
    Class containing methods to make and unmake moves
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
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        moving_piece: int = move.get_moving_piece()
        end_square: int = move.get_end_square()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        move_data: MoveData = MoveMaker.copy_fen_data_to_move_data(board)
        enemy_color: int = ColorManager.get_opposite_piece_color(color)

        if board_array[end_square] == enemy_color | PiecesEnum.ROOK.value:
            FenUtil.disable_castling_on_side(enemy_color, end_square, board)
        if moving_piece == PiecesEnum.ROOK.value:
            MoveMaker.__update_move_data_with_deleted_piece(move_data, board, color, move)
            FenUtil.disable_castling_on_side(board.get_engine_color(), move.get_start_square(), board)

            return move_data
        elif special_flag in SpecialFlags.PROMOTIONS.value:
            MoveMaker.__update_move_data_with_deleted_piece(move_data, board, color, move)
            board_array[end_square] = BoardUtil.get_promotion_piece(color, special_flag)

            return move_data
        elif special_flag in (SpecialFlags.EN_PASSANT.value, SpecialFlags.CASTLING.value):
            deleted_piece = color | moving_piece
            move_data.deleted_piece = deleted_piece

            board.castle_king(deleted_piece, move) if special_flag == SpecialFlags.CASTLING.value else \
                board.make_en_passant_capture(deleted_piece)

            return move_data
        elif moving_piece == PiecesEnum.KING.value:
            MoveMaker.__update_move_data_with_deleted_piece(move_data, board, color, move)
            fen_data.set_castling_king_side(False, board.get_engine_color())
            fen_data.set_castling_queen_side(False, board.get_engine_color())

            return move_data
        else:
            MoveMaker.__update_move_data_with_deleted_piece(move_data, board, color, move)

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
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()
        board_array: ndarray[int, dtype[int8]] = board.get_board_array()
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        deleted_piece: int = deleted_data.deleted_piece
        color: int = ColorManager.get_piece_color(deleted_piece)

        if special_flag == SpecialFlags.CASTLING.value:
            board.un_castle_king(move, color)
            fen_data.update_fen_data(deleted_data)

        elif special_flag in SpecialFlags.PROMOTIONS.value:
            fen_data.update_fen_data(deleted_data)
            color = ColorManager.get_piece_color(board_array[end_square])

            moved_piece = color | move.get_moving_piece()
            board_array[end_square] = deleted_piece
            board_array[start_square] = moved_piece

        else:
            fen_data.update_fen_data(deleted_data)
            moved_piece: int = board_array[end_square]
            board_array[end_square] = deleted_piece
            board_array[start_square] = moved_piece

    @staticmethod
    def __update_board_with_movement(board: 'Board', move: Move, color: int) -> int:
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
    def __update_move_data_with_deleted_piece(move_data: MoveData, board: 'Board', color: int, move: Move) -> None:
        """
        Method used update move data with deleted piece value
        :param move_data: MoveData instance
        :param board: Board instance
        :param color: int value of color
        :param move: Move instance
        :return: None
        """
        deleted_piece = MoveMaker.__update_board_with_movement(board, move, color)
        move_data.deleted_piece = deleted_piece

    @staticmethod
    def copy_fen_data_to_move_data(board: 'Board') -> MoveData:
        """
        Method used to copy fen data for making moves
        :param board: Board instance
        :return: MoveData instance without deleted piece value
        """
        fen_data: FenData = board.get_fen_data()
        white_king, white_queen, black_king, black_queen, en_square, en_piece = fen_data.get_special_move_data()

        return MoveData(MoveEnum.NONE.value, white_king, white_queen, black_king, black_queen, en_square, en_piece)
