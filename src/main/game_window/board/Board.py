from abc import ABC
from abc import abstractmethod
from typing import Tuple

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveData import MoveData
from game_window.moving.generation.data.MoveList import MoveList


class Board(ABC):
    """
    Abstract class for Board representations
    """

    @abstractmethod
    def delete_piece_from_board_square(self, square: int) -> int:
        """
        Deletes piece_square from board and updates fen string.
        :param square:
        :return: deleted piece_square value
        """
        pass

    @abstractmethod
    def add_piece_to_the_board(self, piece: int, square: int) -> None:
        """
        Adds piece_square to board array and updates fen string.
        :param piece: int value of piece_square
        :param square: int index of where to add a piece_square
        :return: None
        """
        pass

    @abstractmethod
    def should_this_piece_move(self, row: int, col: int) -> bool:
        """
        Checks if piece_square on boards row and col indexes should move.
        :param row: int value of row index
        :param col: int value of col index
        :return: bool value if piece_square should move or not
        """
        pass

    @abstractmethod
    def update_legal_moves(self, color: int) -> None:
        """
        Method used to set legal moves_list list
        :param color: int value of color
        :return: None
        """
        pass

    @abstractmethod
    def set_opposite_move_color(self) -> None:
        """
        Method used to change the color of players pieces which is turn.
        :return: None
        """
        pass

    @abstractmethod
    def legal_moves(self) -> MoveList:
        """
        Gives access to legal moves_list list.
        :return: list of moves_list
        """
        pass

    @abstractmethod
    def distances(self) -> ndarray[int, dtype[int8]]:
        """
        Gives access to distances to borders array
        :return: ndarray of distances
        """
        pass

    @abstractmethod
    def board_array(self) -> ndarray[int, dtype[int8]]:
        """
        Gives access to board int array.
        :return: board int array
        """
        pass

    @abstractmethod
    def fen_string(self) -> str:
        """
        Gives access to the fen string.
        :return: fen string
        """
        pass

    @abstractmethod
    def color_to_move(self) -> int:
        """
        Gives access to color which is turn to move
        :return: int value of color
        """
        pass

    @abstractmethod
    def is_it_legal_move(self, move: Move) -> bool:
        """
        Checks if move given can be played
        :param move: current move player wants to play
        :return: bool value whether move is legal or not
        """
        pass

    @abstractmethod
    def update_fen(self) -> None:
        """
        Method used to update fen string with current board state
        :return: None
        """
        pass

    @abstractmethod
    def disable_castling_if_captured_rook(self, deleted_piece: int, color: int, square: int) -> None:
        """
        Method used to disable castling if rook was captured
        :param deleted_piece: int value of deleted piece
        :param color: int value of friendly color
        :param square: int index of rook square
        :return: None
        """
        pass

    @abstractmethod
    def switch_sides(self) -> None:
        """
        Method used to switch sides of board
        :return: None
        """
        pass

    @abstractmethod
    def engine_color(self) -> int:
        """
        Method used to get access to engine color
        :return: int value of engine color
        """
        pass

    @abstractmethod
    def player_color(self) -> int:
        """
        Method used to get access to player color
        :return: int value of player color
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
    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
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
    def en_passant_square(self) -> int:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        pass

    @abstractmethod
    def en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant end_square value
        :return: int value of en passant square
        """
        pass

    @abstractmethod
    def set_en_passant_piece_square(self, piece_square: int) -> None:
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
    def disable_castling_on_side(self, color: int, target_square: int) -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :return: None
        """
        pass

