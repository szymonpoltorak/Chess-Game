from numpy import zeros, ndarray, array

from game_window.BoardInitializer import BoardInitializer
from game_window.enums.BoardEnum import BoardEnum


class Board:
    __slots__ = array(["__board_array", "__fen_string"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value

    def get_board_array(self) -> ndarray[int]:
        """
        Gives access to board int array.
        :return: board int array
        """
        return self.__board_array

    def get_fen_string(self) -> str:
        """
        Gives access to the fen string.
        :return: fen string
        """
        return self.__fen_string

    def __init_starting_board(self) -> ndarray[int]:
        """
        Method initializes starting board.
        :return: board int array
        """
        board = zeros(BoardEnum.BOARD_LENGTH.value ** 2)
        index = 0
        white_pieces = BoardInitializer.init_white_pieces_array()

        black_pieces = BoardInitializer.init_black_pieces_array()

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = black_pieces[index]
            index += 1

        index += 32
        j = 15

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = white_pieces[j]
            j -= 1
            index += 1
        return board
