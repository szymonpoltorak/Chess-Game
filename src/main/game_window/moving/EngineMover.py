from typing import TYPE_CHECKING

from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenUtil import FenUtil
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.pawns.PawnUtil import PawnUtil
from game_window.moving.Move import Move

if TYPE_CHECKING:
    from game_window.board.Board import Board


class EngineMover:
    """
    Class containing methods to update board with engine moves
    """

    @staticmethod
    def update_board_with_engine_move(board: 'Board', computer_move: Move) -> int:
        """
        Updates board with a computer move
        :param board: Board instance
        :param computer_move: Move instance
        :return: int value of deleted piece by computer
        """
        start_square: int = computer_move.get_start_square()
        deleted_piece: int = board.delete_pieces_on_squares(start_square, computer_move.get_end_square())
        special_flag: int = computer_move.get_special_flag_value()
        moving_piece: int = computer_move.get_moving_piece()

        FenUtil.disable_castling_if_deleted_rook(deleted_piece, board.get_player_color(), start_square, board)

        if moving_piece == PiecesEnum.PAWN.value:
            EngineMover.check_pawn_movement(board, computer_move)

        if moving_piece == PiecesEnum.ROOK.value:
            FenUtil.disable_castling_on_side(board.get_engine_color(), start_square, board)
            EngineMover.make_engine_move(computer_move.get_end_square(), moving_piece, board)

        elif PawnUtil.is_it_a_promotion(special_flag):
            EngineMover.make_engine_promotion_move(computer_move, board)

        elif special_flag == SpecialFlags.CASTLING.value:
            piece: int = board.get_engine_color() | moving_piece
            board.castle_king(piece, computer_move)

        elif special_flag == SpecialFlags.EN_PASSANT.value:
            board.make_en_passant_capture(moving_piece)
            deleted_piece = 1
        else:
            EngineMover.make_engine_move(computer_move.get_end_square(), computer_move.get_moving_piece(), board)
        board.set_opposite_move_color()
        board.get_fen_data().update_move_counter()

        FenUtil.update_no_sack_and_pawn_counter(board.get_fen_data(), deleted_piece, moving_piece)

        return deleted_piece

    @staticmethod
    def make_engine_promotion_move(computer_move: Move, board: 'Board') -> None:
        """
        Method used to make a promotion move for a computer
        :param computer_move: computer Move instance
        :param board: Board instance
        :return: None
        """
        promotion_dict = {
            SpecialFlags.PROMOTE_TO_ROOK.value: PiecesEnum.ROOK.value,
            SpecialFlags.PROMOTE_TO_QUEEN.value: PiecesEnum.QUEEN.value,
            SpecialFlags.PROMOTE_TO_BISHOP.value: PiecesEnum.BISHOP.value,
            SpecialFlags.PROMOTE_TO_KNIGHT.value: PiecesEnum.KNIGHT.value
        }
        promotion_piece: int = promotion_dict[computer_move.get_special_flag_value()]
        EngineMover.make_engine_move(computer_move.get_end_square(), promotion_piece, board)

    @staticmethod
    def make_engine_move(end_square: int, piece: int, board: 'Board') -> None:
        """
        Method used to make an engine move
        :param end_square: int value of end square
        :param piece: int value of piece
        :param board: Board instance
        :return: None
        """
        if piece == PiecesEnum.KING.value:
            board.get_fen_data().set_castling_king_side(False, board.get_engine_color())
            board.get_fen_data().set_castling_queen_side(False, board.get_engine_color())
        board.add_piece_to_the_board(board.get_engine_color() + piece, end_square)

    @staticmethod
    def check_pawn_movement(board: 'Board', computer_move: 'Move') -> None:
        """
        Method used to check pawns movement special situations
        :param board: Board instance
        :param computer_move: Move instance of computer move
        :return: None
        """
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
