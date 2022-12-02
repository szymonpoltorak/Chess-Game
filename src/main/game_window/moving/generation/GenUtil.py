from typing import TYPE_CHECKING

from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveList import MoveList

if TYPE_CHECKING:
    from game_window.board.Board import Board


class GenUtil:
    """
    Util static methods for generation
    """

    @staticmethod
    def add_move_if_needed(move_list: MoveList, move: Move, captures_only: bool, board: 'Board') -> None:
        """
        Method used to add new move to the move_list based on if it is a capture only generation or not
        :param move_list: list of moves
        :param move: Move instance
        :param captures_only: decides if method should generate every legal move or captures only
        :param board:
        """
        target_piece: int = board.board_array()[move.get_end_square()]

        if not captures_only:
            move_list.append(move)
        else:
            if target_piece != PiecesEnum.NONE.value:
                move_list.append(move)
