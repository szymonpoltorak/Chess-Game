from typing import TYPE_CHECKING

from numba import jit

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveList import MoveList

if TYPE_CHECKING:
    from game_window.board.Board import Board


class SlidingPiecesGen:
    """
    Class used to generate sliding pieces moves
    """

    __slots__ = ()

    @staticmethod
    @jit(forceobj=True)
    def generate_sliding_piece_moves(piece: int, start_square: int, moves_list: MoveList, color: int, board: 'Board') -> None:
        """
        Static method used to generate moves_list for sliding pieces
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
            for direction_step in range(board.get_distances()[start_square][direction]):
                if not SlidingPiecesGen.is_it_sliding_piece_move(piece, MoveEnum.SLIDING_DIRECTIONS.value[direction]):
                    continue
                move_target: int = start_square + MoveEnum.SLIDING_DIRECTIONS.value[direction] * (direction_step + 1)
                piece_on_move_target: int = board.get_board_array()[move_target]

                if ColorManager.get_piece_color(piece_on_move_target) == color:
                    break
                moves_list.append(Move(start_square, move_target, piece, SpecialFlags.NONE.value))

                if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                    break

    @staticmethod
    def is_it_sliding_piece_move(piece: int, direction: int) -> bool:
        """
        Static method used to check if this move should be calculated
        :param piece: int value of piece_square
        :param direction: int value of direction
        :return: bool value of if move should be calculated or not
        """
        if piece is None or direction is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if not SlidingPiecesGen.is_sliding_piece(piece) or direction not in MoveEnum.SLIDING_DIRECTIONS.value:
            raise IllegalArgumentException("WRONG ARGUMENTS GIVEN TO METHOD!")
        diagonal_pieces: tuple[int, int] = (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value)
        diagonal_directions: tuple[int, int, int, int] = (MoveEnum.TOP_LEFT.value, MoveEnum.TOP_RIGHT.value,
                                                          MoveEnum.BOTTOM_LEFT.value, MoveEnum.BOTTOM_RIGHT.value)

        line_pieces: tuple[int, int] = (PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)
        line_directions: tuple[int, int, int, int] = (MoveEnum.TOP.value, MoveEnum.LEFT.value,
                                                      MoveEnum.RIGHT.value, MoveEnum.BOTTOM.value)

        if piece in diagonal_pieces and direction in diagonal_directions:
            return True
        return piece in line_pieces and direction in line_directions

    @staticmethod
    def is_sliding_piece(piece: int) -> bool:
        """
        Static method used to check if piece_square is a sliding piece_square.
        :param piece: int value of piece_square
        :return: bool value of if piece_square is sliding piece_square or not
        """
        if piece is None:
            raise NullArgumentException("PIECE CANNOT BE NULL!")
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)

