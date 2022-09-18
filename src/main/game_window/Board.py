from numpy import zeros, ndarray, array

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


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
        white_pieces = self.__init_pieces_arrays(PiecesEnum.WHITE.value)

        black_pieces = self.__init_pieces_arrays(PiecesEnum.BLACK.value)

        for index in range(BoardEnum.BOARD_LENGTH.value):
            board[index] = white_pieces[index]

        for index in range(BoardEnum.BOARD_LENGTH.value):
            board[index] = black_pieces[index]
        return board

    def __init_pieces_arrays(self, color_value: int) -> ndarray[int]:
        """
        Initializes array of pieces on starting position depending on given color value.
        :param color_value: white or black int value
        :return: array of starting pieces of given color
        """
        piece_array = array([color_value | PiecesEnum.ROOK.value,
                             color_value | PiecesEnum.KNIGHT.value,
                             color_value | PiecesEnum.BISHOP.value,
                             color_value | PiecesEnum.QUEEN.value,
                             color_value | PiecesEnum.KING.value,
                             color_value | PiecesEnum.BISHOP.value,
                             color_value | PiecesEnum.KNIGHT.value,
                             color_value | PiecesEnum.ROOK.value])
        return piece_array
