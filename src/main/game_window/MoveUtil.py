from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.engine.MoveData import MoveData
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.FenData import FenData
from game_window.Move import Move
from game_window.MoveValidator import MoveValidator

if TYPE_CHECKING:
    from game_window.Board import Board


class MoveUtil:
    __slots__ = ()

    @staticmethod
    def make_move(move: Move, color: int, board: 'Board') -> MoveData:
        # TODO PROMOTION MAY NOT WORK PROPERLY
        """
        Method used to make a given move. It means to update the board int array
        :param board: Board instance
        :param move: Move instance - move we want to make
        :param color: color of a piece
        :return:
        """
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        moving_piece: int = move.get_moving_piece()

        if move.get_moving_piece() == PiecesEnum.ROOK.value:
            move_data: MoveData = MoveUtil.move_and_copy_move_data(board, move, color)
            MoveValidator.disable_castling_on_side(board.get_engine_color(), move, board)

            return move_data
        elif special_flag == SpecialFlags.CASTLING.value:
            deleted_piece: int = color | moving_piece
            white_king, white_queen, black_king, black_queen, en_square, en_piece = fen_data.get_special_move_data()
            board.castle_king(deleted_piece, move)

            return MoveData(deleted_piece, white_king, white_queen, black_king, black_queen, en_square, en_piece)
        elif moving_piece == PiecesEnum.KING.value:
            move_data: MoveData = MoveUtil.move_and_copy_move_data(board, move, color)
            fen_data.set_castling_king_side(False, board.get_engine_color())
            fen_data.set_castling_queen_side(False, board.get_engine_color())

            return move_data
        #elif special_flag == SpecialFlags.EN_PASSANT.value:
        #    pass
        else:
            return MoveUtil.move_and_copy_move_data(board, move, color)

    @staticmethod
    def un_make_move(move: Move, deleted_data: MoveData, board: 'Board') -> None:
        # TODO PROMOTION MAY NOT WORK PROPERLY
        """
        Removes given move with a value of deleted piece
        :param deleted_data:
        :param board:
        :param move: move to be unmade
        :return: None
        """
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()
        board_array: ndarray[int] = board.get_board_array()
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        deleted_piece = deleted_data.deleted_piece
        color: int = ColorManager.get_piece_color(deleted_piece)

        if special_flag == SpecialFlags.CASTLING.value:
            board.un_castle_king(move, color)
            fen_data.update_fen_data(deleted_data)
        else:
            fen_data.update_fen_data(deleted_data)
            moved_piece: int = board_array[end_square]
            board_array[end_square] = deleted_piece
            board_array[start_square] = moved_piece

    @staticmethod
    def move_and_copy_move_data(board: 'Board', move: Move, color: int):
        board_array: ndarray[int] = board.get_board_array()
        fen_data: FenData = board.get_fen_data()
        end_square: int = move.get_end_square()
        white_king, white_queen, black_king, black_queen, en_square, en_piece = fen_data.get_special_move_data()

        deleted_piece: int = board_array[end_square]
        board_array[move.get_start_square()] = 0
        board_array[end_square] = color + move.get_moving_piece()

        return MoveData(deleted_piece, white_king, white_queen, black_king, black_queen, en_square, en_piece)

    @staticmethod
    def update_board_with_engine_move(board: 'Board', computer_move: Move) -> int:
        deleted_piece: int = board.delete_pieces_on_squares(computer_move.get_start_square(),
                                                            computer_move.get_end_square())
        special_flag: int = computer_move.get_special_flag_value()
        moving_piece: int = computer_move.get_moving_piece()

        print(f"Deleted : {deleted_piece}\nMoving : {moving_piece}\n")

        if moving_piece == PiecesEnum.PAWN.value:
            MoveUtil.check_pawn_movement(board, computer_move)

        if moving_piece == PiecesEnum.ROOK.value:
            MoveValidator.disable_castling_on_side(board.get_engine_color(), computer_move, board)
            MoveUtil.make_engine_move(computer_move.get_end_square(), moving_piece, board)
        elif MoveUtil.is_it_a_promotion(special_flag):
            MoveUtil.make_engine_promotion_move(computer_move, board)
        elif special_flag == SpecialFlags.CASTLING.value:
            piece: int = board.get_engine_color() | computer_move.get_moving_piece()
            board.castle_king(piece, computer_move)
        elif special_flag == SpecialFlags.EN_PASSANT.value:
            board.make_en_passant_capture(moving_piece)
            deleted_piece: int = 1
        else:
            MoveUtil.make_engine_move(computer_move.get_end_square(), computer_move.get_moving_piece(), board)
        board.set_opposite_move_color()
        board.get_fen_data().update_move_counter()

        print(f"Deleted : {deleted_piece}\nMoving : {moving_piece}\n")
        MoveUtil.update_no_sack_and_pawn_counter(board.get_fen_data(), deleted_piece, moving_piece)

        return deleted_piece

    @staticmethod
    def is_it_a_promotion(special_flag: int):
        promotions: ndarray[int] = array([SpecialFlags.PROMOTE_TO_ROOK.value, SpecialFlags.PROMOTE_TO_QUEEN.value,
                                          SpecialFlags.PROMOTE_TO_BISHOP.value, SpecialFlags.PROMOTE_TO_KNIGHT.value])
        return special_flag in promotions

    @staticmethod
    def make_engine_promotion_move(computer_move: Move, board: 'Board') -> None:
        promotion_dict = {
            SpecialFlags.PROMOTE_TO_ROOK.value: PiecesEnum.ROOK.value,
            SpecialFlags.PROMOTE_TO_QUEEN.value: PiecesEnum.QUEEN.value,
            SpecialFlags.PROMOTE_TO_BISHOP.value: PiecesEnum.BISHOP.value,
            SpecialFlags.PROMOTE_TO_KNIGHT.value: PiecesEnum.KNIGHT.value
        }
        promotion_piece: int = promotion_dict[computer_move.get_special_flag_value()]
        MoveUtil.make_engine_move(computer_move.get_end_square(), promotion_piece, board)

    @staticmethod
    def make_engine_move(end_square: int, piece: int, board: 'Board') -> None:
        if piece == PiecesEnum.KING.value:
            board.get_fen_data().set_castling_king_side(False, board.get_engine_color())
            board.get_fen_data().set_castling_queen_side(False, board.get_engine_color())
        board.add_piece_to_the_board(board.get_engine_color() + piece, end_square)

    @staticmethod
    def check_pawn_movement(board: 'Board', computer_move: 'Move'):
        move_length: int = computer_move.get_end_square() - computer_move.get_start_square()
        fen_data: FenData = board.get_fen_data()

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
    def update_no_sack_and_pawn_counter(fen_data: FenData, deleted_piece: int, moving_piece: int) -> None:
        if deleted_piece != 0 or moving_piece == PiecesEnum.PAWN.value:
            print("HELLO!")
            fen_data.update_no_sack_and_pawn_count(True)
        elif deleted_piece == 0 or moving_piece != PiecesEnum.PAWN.value:
            print("WTF")
            fen_data.update_no_sack_and_pawn_count(False)
        else:
            raise ValueError("NOT POSSIBLE CONDITION OCCURRED! WRONG PARAMETERS")
