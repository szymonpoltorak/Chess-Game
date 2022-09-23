from numpy import array

from game_window.enums.BoardEnum import BoardEnum


class Move:
    __slots__ = array(["__start_square", "__end_square", "__piece"])

    def __init__(self, start_square: tuple[int, int] or None, end_square: tuple[int, int] or None, piece: int or None):
        self.__start_square = start_square
        self.__end_square = end_square
        self.__piece = piece

    def set_start_square(self, row: int or None, col: int or None) -> None:
        """
        Method to set row and col index of a start movement square
        :param row: int row index of square
        :param col: int col index of square
        :return: None
        """
        if row is None or col is None:
            self.__start_square = None
            return
        start_square = BoardEnum.BOARD_LENGTH.value * row + col
        self.__start_square = start_square

    def set_start_square_with_value(self, start_square: int) -> None:
        """
        Enables to update start square field with single square int value
        :param start_square: int value of square index
        :return: None
        """
        self.__start_square = start_square

    def set_end_square_with_value(self, end_square: int) -> None:
        """
        Enables to update end square field with single square int value
        :param end_square: int value of end square index
        :return: None
        """
        self.__end_square = end_square

    def set_end_square(self, row: int or None, col: int or None) -> None:
        """
        Method to set row and col index of an end movement square
        :param row: int row index of square
        :param col: int col index of square
        :return: None
        """
        if row is None or col is None:
            self.__end_square = None
            return
        end_square = BoardEnum.BOARD_LENGTH.value * row + col
        self.__end_square = end_square

    def get_start_square(self) -> int:
        """
        Gives access to tuple with start move square coordinates
        :return: int start index of piece on board
        """
        return self.__start_square

    def get_end_square(self) -> int:
        """
        Gives access to tuple with end move square coordinates
        :return: int end index of piece on board
        """
        return self.__end_square

    def get_moving_piece(self) -> int:
        """
        Gives access to moving piece value
        :return: int piece value
        """
        return self.__piece

    def set_moving_piece(self, piece: int) -> None:
        """
        Method used to set moving piece.
        :param piece: int value of moving piece
        :return: None
        """
        self.__piece = piece

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False

        if self.__start_square != other.get_start_square() or self.__end_square != other.get_end_square():
            return False
        return self.__piece == other.get_moving_piece()

    def __str__(self):
        return f"StartSquare: {self.__start_square}\nEndSquare: {self.__end_square}\nPiece: {self.__piece}"
