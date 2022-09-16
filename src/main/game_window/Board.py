from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class Board:
    __slots__ = ("__board_array", "__current_fen")

    def __init__(self):
        self.__board_array: list = self.__init_starting_board()
        self.__current_fen: str = BoardEnum.STARTING_POSITION.value
        print(str(self.__board_array))

    def get_board_array(self):
        """
        Gives access to board int list.
        :return: board int list
        """
        return self.__board_array

    def get_fen_string(self):
        """
        Gives access to the fen string.
        :return: fen string
        """
        return self.__current_fen

    def __init_starting_board(self):
        """
        Method initializes starting board.
        :return: board int list
        """
        board = []
        white_pieces = self.__init_pieces_lists(PiecesEnum.WHITE.value)

        black_pieces = self.__init_pieces_lists(PiecesEnum.BLACK.value)

        for index in range(BoardEnum.BOARD_SIZE.value):
            board.append(white_pieces[index])

        for index in range(4 * BoardEnum.BOARD_SIZE.value):
            board.append(PiecesEnum.NONE.value)

        for index in range(BoardEnum.BOARD_SIZE.value):
            board.append(black_pieces[index])
        return board

    def __init_pieces_lists(self, color_value: int):
        """
        Initializes list of pieces on starting position depending on given color calue.
        :param color_value: white or black int value
        :return: list of starting pieces of given color
        """
        return [color_value | PiecesEnum.ROOK.value,
                color_value | PiecesEnum.KNIGHT.value,
                color_value | PiecesEnum.BISHOP.value,
                color_value | PiecesEnum.QUEEN.value,
                color_value | PiecesEnum.KING.value,
                color_value | PiecesEnum.BISHOP.value,
                color_value | PiecesEnum.KNIGHT.value,
                color_value | PiecesEnum.ROOK.value]
