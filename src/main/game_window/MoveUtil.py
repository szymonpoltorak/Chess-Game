from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
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
    def update_board_with_engine_move(board: 'Board', computer_move: Move) -> int:
        deleted_piece = board.delete_pieces_on_squares(computer_move.get_start_square(), computer_move.get_end_square())
        promotions = array([SpecialFlags.PROMOTE_TO_ROOK.value, SpecialFlags.PROMOTE_TO_QUEEN.value,
                            SpecialFlags.PROMOTE_TO_BISHOP.value, SpecialFlags.PROMOTE_TO_KNIGHT.value])

        if computer_move.get_special_flag_value() in promotions:
            MoveUtil.make_engine_promotion_move(computer_move, board)
        else:
            MoveUtil.make_engine_move(computer_move.get_end_square(), computer_move.get_moving_piece(), board)
        return deleted_piece

    @staticmethod
    def make_engine_promotion_move(computer_move: Move, board: 'Board') -> None:
        end_square = computer_move.get_end_square()
        color = board.get_upper_color()
        promotion_dict = {
            SpecialFlags.PROMOTE_TO_ROOK.value: color | PiecesEnum.ROOK.value,
            SpecialFlags.PROMOTE_TO_QUEEN.value: color | PiecesEnum.QUEEN.value,
            SpecialFlags.PROMOTE_TO_BISHOP.value: color | PiecesEnum.BISHOP.value,
            SpecialFlags.PROMOTE_TO_KNIGHT.value: color | PiecesEnum.KNIGHT.value
        }

        promotion_piece = promotion_dict[computer_move.get_special_flag_value()]
        MoveUtil.make_engine_move(end_square, promotion_piece, board)

    @staticmethod
    def make_engine_move(end_square: int, piece: int, board: 'Board') -> None:
        board.add_piece_to_the_board(piece, end_square)
        board.set_opposite_move_color()
        board.update_fen()
