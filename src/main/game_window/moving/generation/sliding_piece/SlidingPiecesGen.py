from typing import TYPE_CHECKING

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveList import MoveList
from game_window.moving.generation.GenUtil import GenUtil
from game_window.moving.generation.sliding_piece.SlidingGenerator import SlidingGenerator
from game_window.moving.generation.sliding_piece.SlidingPiecesUtil import SlidingPiecesUtil

if TYPE_CHECKING:
    from game_window.board.Board import Board


class SlidingPiecesGen(SlidingGenerator):
    """
    Class used to generate sliding pieces __moves
    """

    __slots__ = ()

    def generate_sliding_piece_moves(self, piece: int, start_square: int, moves_list: MoveList, color: int,
                                     board: 'Board', captures_only: bool) -> None:
        """
        Static method used to generate moves_list for sliding pieces
        :param captures_only: decides if method should generate every legal move or captures only
        :param piece: int value of piece_square
        :param start_square: int index of current end_square
        :param moves_list: list of moves_list
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        if None in (piece, start_square, moves_list, color, board):
            raise NullArgumentException("CANNOT GENERATE MOVES WHILE ARGS ARE NULLS!")
        if not ColorManager.is_it_valid_color(color) or piece not in PiecesEnum.PIECES_TUPLE.value or start_square > 63 \
                or start_square < 0:
            raise IllegalArgumentException("GIVEN ARGS ARE NOT WITHIN BONDS!")

        for direction in range(MoveEnum.SLIDING_DIRECTIONS_NUMBER.value):
            for direction_step in range(board.distances()[start_square][direction]):
                if not SlidingPiecesUtil.is_it_sliding_piece_move(piece, MoveEnum.SLIDING_DIRECTIONS.value[direction]):
                    continue
                move_target: int = start_square + MoveEnum.SLIDING_DIRECTIONS.value[direction] * (direction_step + 1)
                piece_on_move_target: int = board.board_array()[move_target]

                if ColorManager.get_piece_color(piece_on_move_target) == color:
                    break
                move: Move = Move(start_square, move_target, piece, SpecialFlags.NONE.value)
                GenUtil.add_move_if_needed(moves_list, move, captures_only, board)

                if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                    break
