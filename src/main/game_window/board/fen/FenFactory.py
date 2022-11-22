from abc import ABC
from abc import abstractmethod
from typing import Tuple
from typing import TYPE_CHECKING

from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData

if TYPE_CHECKING:
    from game_window.board.Board import Board


class FenFactory(ABC):
    """
    Abstract class for fen creation class
    """

    @abstractmethod
    def convert_board_array_to_fen(self, board: 'Board') -> str:
        """
        Method converts int array into fen string
        :param board: Board instance
        :return: fen string
        """
        pass

    @abstractmethod
    def update_no_sack_and_pawn_counter(self, deleted_piece: int, moving_piece: int) -> None:
        """
        Method used to update no sack and pawn move counter
        :param deleted_piece: int value of a piece
        :param moving_piece: int value of a moving piece
        :return: None
        """
        pass

    @abstractmethod
    def disable_castling_on_side(self, color: int, target_square: int, board: 'Board') -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        pass

    @abstractmethod
    def disable_castling_if_captured_rook(self, deleted_piece: int, color: int, square: int, board: 'Board') -> None:
        """
        Method used to disable castling if rook was captured
        :param deleted_piece: int value of deleted piece
        :param color: int value of friendly color
        :param square: int index of rook square
        :param board: Board instance
        :return: None
        """
        pass

    @abstractmethod
    def update_fen_data_with_double_pawn_movement(self, move: Move) -> None:
        """
        Method used to validate double pawn movement in terms of fen data
        :param move: Move instance
        :return None
        """
        pass

    @abstractmethod
    def set_castling_queen_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on queen side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        pass

    @abstractmethod
    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        pass

    @abstractmethod
    def en_passant_square(self) -> int:
        """
        Gives access to an en passant end_square value
        :return: int value of en passant square
        """
        pass

    @abstractmethod
    def en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        pass

    @abstractmethod
    def set_en_passant_square(self, square: int) -> None:
        """
        Method used to set en passant end_square
        :param square: int value of end_square
        :return: None
        """
        pass

    @abstractmethod
    def set_en_passant_piece_square(self, piece_square: int) -> None:
        """
        Method used to set an en passant target piece end_square value
        :param piece_square: int piece end_square value
        :return: None
        """
        pass

    @abstractmethod
    def update_move_counter(self) -> None:
        """
        Increments move counter by 1
        :return: None
        """
        pass

    @abstractmethod
    def can_king_castle_king_side(self, color: int) -> bool:
        """
        Returns if king can castle on king side
        :param color: int value of color
        :return: bool
        """
        pass

    @abstractmethod
    def can_king_castle_queen_side(self, color: int) -> bool:
        """
        Returns if king can castle on queen side
        :param color: int value of color
        :return: bool
        """
        pass

    @abstractmethod
    def get_special_move_data(self) -> Tuple[bool, bool, bool, bool, int, int, int, int]:
        """
        Method used to return a tuple of special fen data for making and unmaking moves_list
        :return: tuple
        """
        pass

    @abstractmethod
    def update_fen_data(self, prev_fen_data: MoveData) -> None:
        """
        Updates fen_data with move_data values
        :param prev_fen_data: MoveData instance
        :return: None
        """
        pass
