from typing import TYPE_CHECKING, Optional

from numba import jit

from game_window.ColorManager import ColorManager
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.pawns.PawnUtil import PawnUtil
from game_window.moving.Move import Move
from game_window.moving.MoveList import MoveList

if TYPE_CHECKING:
    from game_window.board.Board import Board


class PawnGen:
    """
    Class containing methods for pawn move generation
    """

    __slots__ = ()

    @staticmethod
    def generate_pawn_moves(moves_list: MoveList, piece: int, color: int, board: 'Board', start_square: int) -> None:
        """
        Static method to generate moves_list for pawns
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start end_square index
        :return: None
        """
        PawnGen.add_pawn_moves(start_square, piece, color, moves_list, board)
        PawnGen.add_pawn_attacks(start_square, piece, color, moves_list, board)

    @staticmethod
    @jit(forceobj=True)
    def add_pawn_moves(start_square: int, piece: int, color: int, moves_list: MoveList, board: 'Board') -> None:
        """
        Adds possible pawn movements
        :param start_square: int index of starting end_square
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param moves_list: list of moves_list (MoveList instance)
        :param board: Board instance
        :return: None
        """
        move_target: int = start_square
        double_move_target: int = start_square
        direction: int = 1
        pawn_index_bounds_min: int = 48
        pawn_index_bounds_max: int = 55
        upper_color: int = board.get_engine_color()
        down_color: int = ColorManager.get_opposite_piece_color(upper_color)

        if color == down_color:
            if double_move_target < 0 or move_target < 0:
                return
        else:
            if double_move_target > 63 or move_target > 63:
                return
            direction = -1
            pawn_index_bounds_min = 8
            pawn_index_bounds_max = 15

        move_target += direction * MoveEnum.PAWN_UP_SINGLE_MOVE.value
        double_move_target += direction * MoveEnum.PAWN_UP_SINGLE_MOVE.value * 2

        if pawn_index_bounds_min <= start_square <= pawn_index_bounds_max and PawnUtil.no_piece_in_pawns_way(
                double_move_target, start_square, board,
                direction * MoveEnum.PAWN_UP_SINGLE_MOVE.value):
            moves_list.append(Move(start_square, double_move_target, piece, SpecialFlags.NONE.value))
        if board.get_board_array()[move_target] == 0:
            PawnGen.add_moves_and_promotions(start_square, move_target, piece, moves_list)

    @staticmethod
    @jit(forceobj=True)
    def add_pawn_attacks(start_square: int, piece: int, color: int, moves_list: MoveList, board: 'Board') -> None:
        """
        Static method used to add pawn attacks
        :param start_square: int index of starting end_square
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param moves_list: list of moves_list (MoveList instance)
        :param board: Board instance
        :return: None
        """
        engine_color: int = board.get_engine_color()
        left_piece_square: int = start_square + PawnUtil.get_attack_direction(color, "LEFT", engine_color)
        right_piece_square: int = start_square + PawnUtil.get_attack_direction(color, "RIGHT", engine_color)

        if left_piece_square < 0 or left_piece_square > 63 or right_piece_square < 0 or right_piece_square > 63:
            return
        left_piece: int = board.get_board_array()[left_piece_square]
        right_piece: int = board.get_board_array()[right_piece_square]

        if color != ColorManager.get_piece_color(left_piece) and left_piece != PiecesEnum.NONE.value:
            if PawnUtil.is_attack_target_in_border_bounds(start_square, left_piece_square,
                                                          MoveEnum.PAWN_RANGE.value):
                PawnGen.add_moves_and_promotions(start_square, left_piece_square, piece, moves_list)

        if color != ColorManager.get_piece_color(right_piece) and right_piece != PiecesEnum.NONE.value:
            if PawnUtil.is_attack_target_in_border_bounds(start_square, right_piece_square,
                                                          MoveEnum.PAWN_RANGE.value):
                PawnGen.add_moves_and_promotions(start_square, right_piece_square, piece, moves_list)

        PawnGen.check_en_passant_movement(start_square, piece, color, moves_list, board)

    @staticmethod
    def add_moves_and_promotions(start_square: int, move_target: int, piece: int, moves_list: MoveList) -> None:
        """
        Checks if move is a promotion or not and add move to the list
        :param move_target: int target end_square of the move
        :param start_square: int index of starting end_square
        :param piece: int value of a piece_square
        :param moves_list: list of moves_list (MoveList instance)
        :return: None
        """
        if 56 <= move_target <= 63 or 0 <= move_target <= 7:
            for flag in range(SpecialFlags.PROMOTE_TO_QUEEN.value, SpecialFlags.PROMOTE_TO_BISHOP.value + 1):
                moves_list.append(Move(start_square, move_target, piece, flag))
        else:
            moves_list.append(Move(start_square, move_target, piece, SpecialFlags.NONE.value))

    @staticmethod
    def check_en_passant_movement(start_square: int, piece: int, color: int, moves_list: MoveList,
                                  board: 'Board') -> None:
        """
        Checks if there is an en passant movement and add it to list
        :param start_square:
        :param piece: int value of piece
        :param color: int value of color
        :param moves_list: list of moves (MoveList instance)
        :param board: Board instance
        :return: None
        """
        upper_color: int = board.get_engine_color()
        en_passant_square: Optional[int] = board.get_fen_data().get_en_passant_square()
        en_passant_target_left: int = start_square + PawnUtil.get_attack_direction(color, "LEFT", upper_color)
        en_passant_target_right: int = start_square + PawnUtil.get_attack_direction(color, "RIGHT", upper_color)

        if en_passant_square == -1:
            return
        if en_passant_square == en_passant_target_left:
            moves_list.append(Move(start_square, en_passant_target_left, piece, SpecialFlags.EN_PASSANT.value))
        elif en_passant_square == en_passant_target_right:
            moves_list.append(Move(start_square, en_passant_target_right, piece, SpecialFlags.EN_PASSANT.value))
