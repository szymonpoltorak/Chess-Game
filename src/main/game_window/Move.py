from numpy import array


class Move:
    __slots__ = array(["__is_piece_moving", "__start_square", "__end_square"])

    def __init__(self):
        self.__is_piece_moving = False
        self.__start_square = None
        self.__end_square = None

    def get_start_square(self) -> tuple[int, int] or None:
        """
        Gives access to tuple with start move square coordinates
        :return: tuple with (row, col) indexes
        """
        return self.__start_square

    def get_end_square(self) -> tuple[int, int] or None:
        """
        Gives access to tuple with end move square coordinates
        :return: tuple with (row, col) indexes
        """
        return self.__end_square

    def if_piece_is_moving(self) -> bool:
        return self.__is_piece_moving

    def set_piece_movement(self, movement: bool) -> None:
        self.__is_piece_moving = movement

    def set_start_square(self, row: int, col: int) -> None:
        """
        Method to set row and col index of a start movement square
        :param row: int row index of square
        :param col: int col index of square
        :return: None
        """
        self.__start_square = (row, col)

    def set_end_square(self, row: int, col: int) -> None:
        """
        Method to set row and col index of an end movement square
        :param row: int row index of square
        :param col: int col index of square
        :return: None
        """
        self.__end_square = (row, col)
