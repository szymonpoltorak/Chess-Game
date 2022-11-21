from typing import Tuple
from typing import TYPE_CHECKING

from game_window.board.BoardUtil import BoardUtil
from game_window.board.fen.FenData import FenData
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.pawns.PawnUtil import PawnUtil
from game_window.moving.Move import Move
from game_window.moving.MoveList import MoveList

if TYPE_CHECKING:
    from game_window.board.Board import Board


class KingKnightGen:
    """
    Class containing methods to generate __moves for Knights and Kings
    """

    __slots__ = ()

    @staticmethod
    def generate_moves_for_knight_and_king(moves_list: MoveList, piece: int, color: int, board: 'Board',
                                           start_square: int) -> None:
        """
        Static method used to generate moves_list for knights and kings
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of piece_square
        :param color: int value of color to move
        :param board: board instance
        :param start_square: int index of current end_square
        :return: None
        """
        if piece == PiecesEnum.KING.value:
            directions: Tuple[int, ...] = MoveEnum.KING_DIRECTIONS.value
            piece_range: int = MoveEnum.KING_RANGE.value
        else:
            directions = MoveEnum.KNIGHT_DIRECTIONS.value
            piece_range = MoveEnum.MAX_KNIGHT_JUMP.value

        for direction in range(MoveEnum.KK_DIRECTIONS_NUMBER.value):
            move_target: int = start_square + directions[direction]

            if move_target > BoardEnum.BOARD_SIZE.value - 1 or move_target < 0:
                continue

            if not PawnUtil.is_attack_target_in_border_bounds(start_square, move_target, piece_range):
                continue
            piece_on_move_target: int = board.get_board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            moves_list.append(Move(start_square, move_target, piece, SpecialFlags.NONE.value))

        if piece == PiecesEnum.KING.value:
            KingKnightGen.generate_castling_moves(moves_list, piece, color, board, start_square)

    @staticmethod
    def generate_castling_moves(moves_list: MoveList, piece: int, color: int, board: 'Board',
                                start_square: int) -> None:
        """
        Static method to generate castling moves_list
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start end_square index
        :return: None
        """
        fen_data: FenData = board.get_fen_data()

        if not KingUtil.is_anything_on_king_side(board, start_square) and fen_data.can_king_castle_king_side(
                color):
            if not BoardUtil.is_board_inverted(board):
                move_target: int = start_square + MoveEnum.CASTLE_MOVE.value
            else:
                move_target = start_square - MoveEnum.CASTLE_MOVE.value
            moves_list.append(Move(start_square, move_target, piece, SpecialFlags.CASTLING.value))

        if not KingUtil.is_anything_on_queen_side(board, start_square) and fen_data.can_king_castle_queen_side(
                color):
            if not BoardUtil.is_board_inverted(board):
                move_target = start_square - MoveEnum.CASTLE_MOVE.value
            else:
                move_target = start_square + MoveEnum.CASTLE_MOVE.value
            moves_list.append(Move(start_square, move_target, piece, SpecialFlags.CASTLING.value))
