from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.Move import Move
from game_window.MoveValidator import MoveValidator

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
        special_flag = computer_move.get_special_flag_value()
        moving_piece = computer_move.get_moving_piece()

        if moving_piece == PiecesEnum.PAWN.value:
            MoveUtil.check_pawn_movement(board, computer_move)
        if moving_piece == PiecesEnum.ROOK.value:
            MoveValidator.disable_castling_on_side(board.get_engine_color(), computer_move, board)
            MoveUtil.make_engine_move(computer_move.get_end_square(), moving_piece, board)
        elif special_flag in promotions:
            MoveUtil.make_engine_promotion_move(computer_move, board)
        elif special_flag == SpecialFlags.CASTLING.value:
            piece = board.get_engine_color() | computer_move.get_moving_piece()
            board.castle_king(piece, computer_move)
        elif special_flag == SpecialFlags.EN_PASSANT.value:
            board.make_en_passant_capture(moving_piece)
        else:
            MoveUtil.make_engine_move(computer_move.get_end_square(), computer_move.get_moving_piece(), board)
        return deleted_piece

    @staticmethod
    def make_engine_promotion_move(computer_move: Move, board: 'Board') -> None:
        promotion_dict = {
            SpecialFlags.PROMOTE_TO_ROOK.value: PiecesEnum.ROOK.value,
            SpecialFlags.PROMOTE_TO_QUEEN.value: PiecesEnum.QUEEN.value,
            SpecialFlags.PROMOTE_TO_BISHOP.value: PiecesEnum.BISHOP.value,
            SpecialFlags.PROMOTE_TO_KNIGHT.value: PiecesEnum.KNIGHT.value
        }
        promotion_piece = promotion_dict[computer_move.get_special_flag_value()]
        MoveUtil.make_engine_move(computer_move.get_end_square(), promotion_piece, board)

    @staticmethod
    def make_engine_move(end_square: int, piece: int, board: 'Board') -> None:
        if piece == PiecesEnum.KING.value:
            board.get_fen_data().set_castling_king_side(False, board.get_engine_color())
            board.get_fen_data().set_castling_queen_side(False, board.get_engine_color())

        board.add_piece_to_the_board(board.get_engine_color() + piece, end_square)
        board.set_opposite_move_color()
        board.update_fen()

    @staticmethod
    def check_pawn_movement(board: 'Board', computer_move: 'Move'):
        move_length = computer_move.get_end_square() - computer_move.get_start_square()
        fen_data = board.get_fen_data()

        if move_length == MoveEnum.PAWN_UP_DOUBLE_MOVE.value:
            fen_data.set_en_passant_square(computer_move.get_end_square() - MoveEnum.PAWN_UP_SINGLE_MOVE.value)
            fen_data.set_en_passant_piece_square(computer_move.get_end_square())
        elif move_length == MoveEnum.PAWN_DOWN_DOUBLE_MOVE.value:
            fen_data.set_en_passant_square(computer_move.get_end_square() - MoveEnum.PAWN_DOWN_SINGLE_MOVE.value)
            fen_data.set_en_passant_piece_square(computer_move.get_end_square())
        elif fen_data.get_en_passant_square() != -1:
            fen_data.set_en_passant_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
            fen_data.set_en_passant_piece_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)

    @staticmethod
    def make_en_passant_move():
        print()
