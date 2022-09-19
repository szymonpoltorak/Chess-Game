from numpy import array
from numpy import ndarray
from numpy import zeros

from game_window.BoardInitializer import BoardInitializer
from game_window.enums.BoardEnum import BoardEnum
from game_window.FenFactory import FenFactory


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        print(self.__board_array)

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

    def delete_piece_from_board(self, row: int, col: int) -> int:
        """
        Deletes piece from board and updates fen string.
        :param row: row int index
        :param col: col int index
        :return: deleted piece value
        """
        board_index = BoardEnum.BOARD_LENGTH.value * row + col

        piece = self.__board_array[board_index]
        self.__board_array[board_index] = 0
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)

        return piece

    def add_piece_to_the_board(self, piece: int, row: int, col: int) -> None:
        """
        Adds piece to board array and updates fen string.
        :param piece: int value of piece
        :param row: int row index
        :param col: int col index
        :return: None
        """
        board_index = BoardEnum.BOARD_LENGTH.value * row + col

        self.__board_array[board_index] = piece
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)
