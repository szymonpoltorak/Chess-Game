from typing import TYPE_CHECKING

from numba import jit
from numpy import full

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.king_and_knights.KingKnightGen import KingKnightGen
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.pawns.PawnGen import PawnGen
from game_window.moving.generation.sliding_piece.SlidingPiecesGen import SlidingPiecesGen
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveList import MoveList
from game_window.moving.MoveMaker import MoveMaker

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveGenerator:
    """
    Class used for generating moves
    """

    __slots__ = ()

    @staticmethod
    def generate_legal_moves(color_to_move: int, board: 'Board') -> MoveList:
        """
        Method used to generate legal moves for current position for given player
        :param color_to_move: player color int
        :param board: Board instance
        :return: MoveList
        """
        pseudo_legal_moves: MoveList = MoveGenerator.generate_moves(color_to_move, board)
        legal_moves: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

        for move_to_verify in pseudo_legal_moves:
            if move_to_verify is None:
                break
            is_it_valid_move: bool = True
            deleted_data: MoveData = MoveMaker.make_move(move_to_verify, color_to_move, board)
            opponent_moves: MoveList = MoveGenerator.generate_moves(ColorManager.get_opposite_piece_color(color_to_move), board)
            kings_square: int = KingUtil.find_friendly_king_squares(board.get_board_array(), color_to_move)

            for move in opponent_moves:
                special_flag: int = move_to_verify.get_special_flag_value()

                if move is None:
                    break
                end_square: int = move.get_end_square()

                if special_flag == SpecialFlags.CASTLING.value and end_square in KingUtil.get_castling_squares(move_to_verify):
                    is_it_valid_move = False
                    break
                if end_square == kings_square:
                    is_it_valid_move = False
                    break
            if is_it_valid_move:
                legal_moves.append(move_to_verify)
            MoveMaker.un_make_move(move_to_verify, deleted_data, board)

        return legal_moves

    @staticmethod
    @jit(forceobj=True)
    def generate_moves(color_to_move: int, board: 'Board') -> MoveList:
        """
        Static method used  to generate legal moves_list for pieces of given color
        :param color_to_move: int value of color to be moved
        :param board: Board instance == representation of board
        :return: list of all legal moves
        """
        moves_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

        for square in range(BoardEnum.BOARD_SIZE.value):
            piece_color: int = ColorManager.get_piece_color(board.get_board_array()[square])
            piece: int = board.get_board_array()[square] - piece_color

            if color_to_move != piece_color:
                continue

            if SlidingPiecesGen.is_sliding_piece(piece):
                SlidingPiecesGen.generate_sliding_piece_moves(piece, square, moves_list, color_to_move, board)
            elif piece == PiecesEnum.KNIGHT.value or piece == PiecesEnum.KING.value:
                KingKnightGen.generate_moves_for_knight_and_king(moves_list, piece, color_to_move, board, square)
            elif piece == PiecesEnum.PAWN.value:
                PawnGen.generate_pawn_moves(moves_list, piece, color_to_move, board, square)
        return moves_list
