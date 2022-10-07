from typing import TYPE_CHECKING

from numpy import ndarray

from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move

if TYPE_CHECKING:
    from game_window.Board import Board


class MoveUtil:
    @staticmethod
    def make_move(move: Move, color: int, board_array: ndarray[int]) -> int:
        """
        Method used to make a given move. It means to update the board int array
        :param board_array: array of ints
        :param move: Move instance - move we want to make
        :param color: color of a piece
        :return: int value of deleted piece
        """
        deleted_piece: int = board_array[move.get_end_square()]

        board_array[move.get_start_square()] = 0
        board_array[move.get_end_square()] = color + move.get_moving_piece()

        return deleted_piece

    @staticmethod
    def un_make_move(move: Move, deleted_piece: int, board_array: ndarray[int]) -> None:
        """
        Removes given move with a value of deleted piece
        :param board_array: array of ints
        :param move: move to be unmade
        :param deleted_piece: deleted piece in move value
        :return: None
        """
        end_square = move.get_end_square()

        moved_piece = board_array[end_square]
        board_array[end_square] = deleted_piece
        board_array[move.get_start_square()] = moved_piece

    @staticmethod
    def make_engine_move(board: 'Board', computer_move: Move):
        deleted_piece = board.delete_pieces_on_squares(computer_move.get_start_square(), computer_move.get_end_square())
        board.add_piece_to_the_board(PiecesEnum.BLACK.value + computer_move.get_moving_piece(), computer_move.get_end_square())
        board.set_opposite_move_color()
        board.update_fen()

        return deleted_piece
