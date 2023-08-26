from typing import TYPE_CHECKING

from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.enums.SpecialFlags import SpecialFlags
from src.main.game_window.moving.MoveMaker import MoveMaker
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.data.MoveData import MoveData

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class EngineMover:
    """
    Class containing methods to update board with engine moves
    """

    __slots__ = ()

    @staticmethod
    def update_board_with_engine_move(board: 'Board', computer_move: Move) -> int:
        """
        Method used to update board with engines move
        :param board:
        :param computer_move: Move instance of computer move
        :return: int value of deleted piece
        """
        moving_piece: int = computer_move.get_moving_piece()

        move_data: MoveData = MoveMaker.make_move(computer_move, board.engine_color(), board)
        board.set_opposite_move_color()
        board.update_move_counter()
        board.update_no_sack_and_pawn_counter(move_data.deleted_piece, moving_piece)

        return PiecesEnum.NONE.value if computer_move.get_special_flag() == SpecialFlags.CASTLING.value else \
            move_data.deleted_piece
