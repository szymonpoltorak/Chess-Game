from typing import TYPE_CHECKING
from typing import Tuple

from src.main.game_window.ColorManager import ColorManager
from src.main.game_window.board.BoardUtil import BoardUtil
from src.main.game_window.enums.BoardEnum import BoardEnum
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.enums.SpecialFlags import SpecialFlags
from src.main.game_window.moving.generation.GenUtil import GenUtil
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.data.MoveList import MoveList
from src.main.game_window.moving.generation.king_and_knights.KingKnightGenerator import KingKnightGenerator
from src.main.game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from src.main.game_window.moving.generation.pawns.PawnUtil import PawnUtil

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class KingKnightGen(KingKnightGenerator):
    """
    Class containing methods to generate __moves for Knights and Kings
    """

    __slots__ = ()

    def generate_moves_for_knight_and_king(self, moves_list: MoveList, piece: int, color: int, board: 'Board',
                                           start_square: int, captures_only: bool) -> None:
        """
        Static method used to generate moves_list for knights and kings
        :param captures_only: decides if method should generate every legal move or captures only
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
            piece_on_move_target: int = board.board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            move: Move = Move(start_square, move_target, piece, SpecialFlags.NONE.value)
            GenUtil.add_move_if_needed(moves_list, move, captures_only, board)

        if piece == PiecesEnum.KING.value and not captures_only:
            self.__generate_castling_moves(moves_list, piece, color, board, start_square)

    def __generate_castling_moves(self, moves_list: MoveList, piece: int, color: int, board: 'Board',
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
        if not KingUtil.is_anything_on_king_side(board, start_square) and board.can_king_castle_king_side(color):
            if not BoardUtil.is_board_inverted(board):
                move_target: int = start_square + MoveEnum.CASTLE_MOVE.value
            else:
                move_target = start_square - MoveEnum.CASTLE_MOVE.value
            moves_list.append(Move(start_square, move_target, piece, SpecialFlags.CASTLING.value))

        if not KingUtil.is_anything_on_queen_side(board, start_square) and board.can_king_castle_queen_side(color):
            if not BoardUtil.is_board_inverted(board):
                move_target = start_square - MoveEnum.CASTLE_MOVE.value
            else:
                move_target = start_square + MoveEnum.CASTLE_MOVE.value
            moves_list.append(Move(start_square, move_target, piece, SpecialFlags.CASTLING.value))
