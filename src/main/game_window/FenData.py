from numpy import array

from game_window.enums.PiecesEnum import PiecesEnum


class FenData:
    __slots__ = array(["__white_castle_king", "__white_castle_queen", "__black_castle_king", "__black_castle_queen",
                       "__en_passant_square", "__en_passant_piece_square", "__move_counter",
                       "__no_sack_and_pawn_count"])

    def __init__(self):
        self.__white_castle_king = True
        self.__white_castle_queen = True
        self.__black_castle_king = True
        self.__black_castle_queen = True
        self.__en_passant_square = -1
        self.__en_passant_piece_square = -1
        self.__move_counter = 1
        self.__no_sack_and_pawn_count = 0

    def can_king_castle_king_side(self, color: int) -> bool:
        """
        Returns if king can castle on king side
        :param color: int value of color
        :return: bool
        """
        return self.__white_castle_king if color == PiecesEnum.WHITE.value else self.__black_castle_king

    def can_king_castle_queen_side(self, color: int) -> bool:
        """
        Returns if king can castle on queen side
        :param color: int value of color
        :return: bool
        """
        return self.__white_castle_queen if color == PiecesEnum.WHITE.value else self.__black_castle_queen

    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        if color == PiecesEnum.WHITE.value:
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
        Gives access to counter of how many moves have passed since last pawn move or any sack
        :return: int value of counter
        """
        return self.__no_sack_and_pawn_count

    def update_no_sack_and_pawn_count(self, to_zero: bool) -> None:
        """
        Updates no sack and no pawn move counter or makes it equal to 0
        :param to_zero: bool value if counter should be made 0 or not
        :return: None
        """
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
        if color == PiecesEnum.WHITE.value:
            self.__white_castle_queen = can_castle
        else:
            self.__black_castle_queen = can_castle

    def set_en_passant_square(self, square: int) -> None:
        """
        Method used to set en passant end_square
        :param square: int value of end_square
        :return: None
        """
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
        :return:
        """
        return self.__en_passant_square

    def get_en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant piece end_square value
        :return:
        """
        return self.__en_passant_piece_square
