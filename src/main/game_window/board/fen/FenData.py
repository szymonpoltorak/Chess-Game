from numpy import array
from typing import Tuple

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.moving.MoveData import MoveData


class FenData:
    """
    Class used to containing data for fen creation
    """

    __slots__ = array(["__white_castle_king", "__white_castle_queen", "__black_castle_king", "__black_castle_queen",
                       "__en_passant_square", "__en_passant_piece_square", "__move_counter",
                       "__no_sack_and_pawn_count", "__player_color"], dtype=str)

    def __init__(self, player_color: int):
        self.__white_castle_king: bool = True
        self.__white_castle_queen: bool = True
        self.__black_castle_king: bool = True
        self.__black_castle_queen: bool = True
        self.__en_passant_square: int = -1
        self.__en_passant_piece_square: int = -1
        self.__move_counter: int = 0
        self.__no_sack_and_pawn_count: int = 0
        self.__player_color: int = player_color

    def can_king_castle_king_side(self, color: int) -> bool:
        """
        Returns if king can castle on king side
        :param color: int value of color
        :return: bool
        """
        if color is None:
            raise NullArgumentException("COLOR CANNOT BE NULL!")
        if not ColorManager.is_it_valid_color(color):
            raise IllegalArgumentException("WRONG COLOR ARGUMENT!")
        return self.__white_castle_king if color == self.__player_color else self.__black_castle_king

    def can_king_castle_queen_side(self, color: int) -> bool:
        """
        Returns if king can castle on queen side
        :param color: int value of color
        :return: bool
        """
        if color is None:
            raise NullArgumentException("COLOR CANNOT BE NULL!")
        if not ColorManager.is_it_valid_color(color):
            raise IllegalArgumentException("WRONG COLOR ARGUMENT!")
        return self.__white_castle_queen if color == self.__player_color else self.__black_castle_queen

    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        if color is None or can_castle is None:
            raise NullArgumentException("COLOR AND CAN_CASTLE CANNOT BE NULLS!")
        if not ColorManager.is_it_valid_color(color):
            raise IllegalArgumentException("WRONG COLOR ARGUMENT!")

        if color == self.__player_color:
            self.__white_castle_king = can_castle
        else:
            self.__black_castle_king = can_castle

    def update_move_counter(self) -> None:
        """
        Increments move counter by 1
        :return: None
        """
        self.__move_counter += 1

    def get_move_counter(self) -> int:
        """
        Gives access to move counter current value
        :return: int value of counter
        """
        return self.__move_counter

    def get_no_sack_and_pawn_count(self) -> int:
        """
        Gives access to counter of how many moves_list have passed since last pawn move or any sack
        :return: int value of counter
        """
        return self.__no_sack_and_pawn_count

    def update_no_sack_and_pawn_count(self, to_zero: bool) -> None:
        """
        Updates no sack and no pawn move counter or makes it equal to 0
        :param to_zero: bool value if counter should be made 0 or not
        :return: None
        """
        if to_zero is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")

        if to_zero:
            self.__no_sack_and_pawn_count = 0
            return
        self.__no_sack_and_pawn_count += 1

    def set_castling_queen_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on queen side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        if color is None or can_castle is None:
            raise NullArgumentException("COLOR AND CAN_CASTLE CANNOT BE NULLS!")
        if color not in (8, 16):
            raise IllegalArgumentException("WRONG COLOR ARGUMENT!")

        if color == self.__player_color:
            self.__white_castle_queen = can_castle
        else:
            self.__black_castle_queen = can_castle

    def set_en_passant_square(self, square: int) -> None:
        """
        Method used to set en passant end_square
        :param square: int value of end_square
        :return: None
        """
        if square is None:
            raise NullArgumentException("SQUARE CANNOT BE NULL!")
        if square < -1 or square > 63:
            raise IllegalArgumentException("SQUARE IS NOT WITHIN BONDS!")
        self.__en_passant_square = square

    def set_en_passant_piece_square(self, piece_square: int) -> None:
        """
        Method used to set an en passant target piece end_square value
        :param piece_square: int piece end_square value
        :return: None
        """
        self.__en_passant_piece_square = piece_square

    def get_en_passant_square(self) -> int:
        """
        Gives access to an en passant end_square value
        :return: int value of en passant square
        """
        return self.__en_passant_square

    def get_en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        return self.__en_passant_piece_square

    def get_special_move_data(self) -> Tuple[bool, bool, bool, bool, int, int]:
        """
        Method used to return a tuple of special fen data for making and unmaking moves_list
        :return: tuple
        """
        return self.__white_castle_king, self.__white_castle_queen, self.__black_castle_king, \
               self.__black_castle_queen, self.__en_passant_square, self.__en_passant_piece_square

    def update_fen_data(self, prev_fen_data: MoveData) -> None:
        """
        Updates fen_data with move_data values
        :param prev_fen_data: MoveData instance
        :return: None
        """
        if prev_fen_data is None:
            raise NullArgumentException("MOVE DATA CANNOT BE NULL!")

        self.__white_castle_king = prev_fen_data.white_castle_king
        self.__white_castle_queen = prev_fen_data.white_castle_queen
        self.__black_castle_king = prev_fen_data.black_castle_king
        self.__black_castle_queen = prev_fen_data.black_castle_queen
        self.__en_passant_square = prev_fen_data.en_passant_square
        self.__en_passant_piece_square = prev_fen_data.en_passant_piece_square

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FenData):
            return False
        if self.__player_color != other.__player_color or self.__en_passant_square != other.__en_passant_square:
            return False
        if self.__en_passant_piece_square != other.__en_passant_piece_square or self.__move_counter != other.__move_counter:
            return False
        if self.__no_sack_and_pawn_count != other.__no_sack_and_pawn_count or self.__white_castle_queen != other.__white_castle_queen:
            return False
        if self.__white_castle_king != other.__white_castle_king or self.__black_castle_queen != other.__black_castle_queen:
            return False
        return self.__black_castle_king == other.__black_castle_king

    def __hash__(self) -> int:
        return hash(
            (self.__black_castle_king, self.__black_castle_queen, self.__white_castle_queen, self.__white_castle_king,
             self.__move_counter, self.__no_sack_and_pawn_count, self.__en_passant_piece_square,
             self.__en_passant_square, self.__player_color))
