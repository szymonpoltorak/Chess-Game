from numpy import array

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum


class Move:
    """
    Class representation of a Move
    """

    __slots__ = array(["__start_square", "__end_square", "__piece", "__special_flag"], dtype=str)

    def __init__(self, start_square: int, end_square: int, piece: int, special_flag: int) -> None:
        self.__start_square: int = start_square
        self.__end_square: int = end_square
        self.__piece: int = piece
        self.__special_flag: int = special_flag

    def set_special_flag(self, special_flag: int) -> None:
        """
        Method used to set the special flag
        :param special_flag:
        :return: None
        """
        self.__special_flag = special_flag

    def set_start_square(self, row: int, col: int) -> None:
        """
        Method to set row and col index of a start movement end_square
        :param row: int row index of end_square
        :param col: int col index of end_square
        :return: None
        """
        if MoveEnum.NONE.value in (row, col):
            self.__start_square = MoveEnum.NONE.value
        else:
            self.__start_square = BoardEnum.BOARD_LENGTH.value * row + col

    def set_end_square(self, row: int, col: int) -> None:
        """
        Method to set row and col index of an end movement end_square
        :param row: int row index of end_square
        :param col: int col index of end_square
        :return: None
        """
        if MoveEnum.NONE.value in (row, col):
            self.__end_square = MoveEnum.NONE.value
        else:
            self.__end_square = BoardEnum.BOARD_LENGTH.value * row + col

    def get_special_flag_value(self) -> int:
        """
        Returns the value of special move flag which stands for special move value
        :return: int value of special flag
        """
        return self.__special_flag

    def get_start_square(self) -> int:
        """
        Gives access to tuple with start move end_square coordinates
        :return: int start index of piece_square on board
        """
        return self.__start_square

    def get_end_square(self) -> int:
        """
        Gives access to tuple with end move end_square coordinates
        :return: int end index of piece_square on board
        """
        return self.__end_square

    def get_moving_piece(self) -> int:
        """
        Gives access to moving piece_square value
        :return: int piece_square value
        """
        return self.__piece

    def set_moving_piece(self, piece: int) -> None:
        """
        Method used to set moving piece_square.
        :param piece: int value of moving piece_square
        :return: None
        """
        self.__piece = piece

    def __eq__(self, other: object) -> bool:
        """
        Magic method used to check if objects are equals
        :param other: object to compare
        :return: bool
        """
        if not isinstance(other, Move):
            return False

        if self.__start_square != other.get_start_square() or self.__end_square != other.get_end_square():
            return False
        return self.__piece == other.get_moving_piece()

    def __str__(self) -> str:
        """
        Magic method with toString
        :return: string representation of class
        """
        return f"\tStartSquare : {self.__start_square}\n\tEndSquare : {self.__end_square}\n\tPiece : {self.__piece}\n" \
               f"\tSpecialFlag : {self.__special_flag}\n"
