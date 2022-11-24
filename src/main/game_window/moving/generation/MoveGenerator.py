from typing import TYPE_CHECKING

from numpy import full

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.Generator import Generator
from game_window.moving.generation.king_and_knights.KingKnightGen import KingKnightGen
from game_window.moving.generation.king_and_knights.KingKnightGenerator import KingKnightGenerator
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.pawns.PawnGen import PawnGen
from game_window.moving.generation.pawns.PawnGenerator import PawnGenerator
from game_window.moving.generation.sliding_piece.SlidingGenerator import SlidingGenerator
from game_window.moving.generation.sliding_piece.SlidingPiecesGen import SlidingPiecesGen
from game_window.moving.generation.data.MoveList import MoveList
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveData import MoveData
from game_window.moving.generation.data.Moves import Moves
from game_window.moving.generation.sliding_piece.SlidingPiecesUtil import SlidingPiecesUtil
from game_window.moving.MoveMaker import MoveMaker

if TYPE_CHECKING:
    from game_window.board.Board import Board


class MoveGenerator(Generator):
    """
    Class used for generating __moves
    """

    __slots__ = ("__pawn_gen", "__king_knight", "__sliding_gen")

    def __init__(self) -> None:
        self.__pawn_gen: PawnGenerator = PawnGen()
        self.__king_knight: KingKnightGenerator = KingKnightGen()
        self.__sliding_gen: SlidingGenerator = SlidingPiecesGen()

    def generate_legal_moves(self, color_to_move: int, board: 'Board') -> MoveList:
        """
        Method used to generate legal __moves for current position for given player
        :param color_to_move: player color int
        :param board: Board instance
        :return: MoveList
        """
        pseudo_legal_moves: MoveList = self.__generate_moves(color_to_move, board)
        legal_moves: MoveList = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object))

        for index in range(pseudo_legal_moves.size()):
            move_to_verify: Move = pseudo_legal_moves[index]
            is_it_valid_move: bool = True
            deleted_data: MoveData = MoveMaker.make_move(move_to_verify, color_to_move, board)
            opponent_moves: MoveList = self.__generate_moves(ColorManager.get_opposite_piece_color(color_to_move), board)
            kings_square: int = KingUtil.find_friendly_king_squares(board.board_array(), color_to_move)

            for j in range(opponent_moves.size()):
                move: Move = opponent_moves[j]
                special_flag: int = move_to_verify.get_special_flag()
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

    def __generate_moves(self, color_to_move: int, board: 'Board') -> MoveList:
        """
        Static method used  to generate legal moves_list for pieces of given color
        :param color_to_move: int value of color to be moved
        :param board: Board instance == representation of board
        :return: list of all legal __moves
        """
        moves_list: MoveList = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object))

        for square in range(BoardEnum.BOARD_SIZE.value):
            piece_color: int = ColorManager.get_piece_color(board.board_array()[square])
            piece: int = board.board_array()[square] - piece_color

            if color_to_move != piece_color:
                continue

            if SlidingPiecesUtil.is_it_sliding_piece(piece):
                self.__sliding_gen.generate_sliding_piece_moves(piece, square, moves_list, color_to_move, board)
            elif piece in (PiecesEnum.KING.value, PiecesEnum.KNIGHT.value):
                self.__king_knight.generate_moves_for_knight_and_king(moves_list, piece, color_to_move, board, square)
            elif piece == PiecesEnum.PAWN.value:
                self.__pawn_gen.generate_pawn_moves(moves_list, piece, color_to_move, board, square)
        return moves_list
