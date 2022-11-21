from typing import TYPE_CHECKING

from game_window.board.fen.FenUtil import FenUtil
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveMaker import MoveMaker

if TYPE_CHECKING:
    from game_window.board.Board import Board


class EngineMover:
    """
    Class containing methods to update board with engine __moves
    """
    @staticmethod
    def update_board_with_engine_move(board: 'Board', computer_move: Move) -> int:
        """
        Method used to update board with engines move
        :param board:
        :param computer_move: Move instance of computer move
        :return: int value of deleted piece
        """
        moving_piece: int = computer_move.get_moving_piece()

        move_data: MoveData = MoveMaker.make_move(computer_move, board.get_engine_color(), board)
        board.set_opposite_move_color()
        board.get_fen_data().update_move_counter()
        FenUtil.update_no_sack_and_pawn_counter(board.get_fen_data(), move_data.deleted_piece, moving_piece)

        return PiecesEnum.NONE.value if computer_move.get_special_flag() == SpecialFlags.CASTLING.value else \
            move_data.deleted_piece
