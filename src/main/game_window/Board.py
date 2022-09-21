from numpy import array
from numpy import ndarray
from numpy import zeros

from game_window.BoardInitializer import BoardInitializer
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.FenFactory import FenFactory
from game_window.Move import Move
from game_window.MoveValidator import MoveValidator


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders = MoveValidator.calculate_distance_to_borders()
        self.__legal_moves = MoveValidator.generate_legal_moves(self.__color_to_move, self)

    def set_legal_moves(self, legal_moves: list[Move]) -> None:
        self.__legal_moves = legal_moves

    def set_opposite_move_color(self) -> None:
        if self.__color_to_move == PiecesEnum.BLACK.value:
            self.__color_to_move = PiecesEnum.WHITE.value
        else:
            self.__color_to_move = PiecesEnum.BLACK.value

    def get_legal_moves(self) -> list[Move]:
        return self.__legal_moves

    def get_distances(self) -> ndarray[int]:
        return self.__distances_to_borders

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

    def get_color_to_move(self) -> int:
        return self.__color_to_move

    def __init_starting_board(self) -> ndarray[int]:
        """
        Method initializes starting board.
        :return: board int array
        """
        board = zeros(BoardEnum.BOARD_SIZE.value)
        index = 0
        white_pieces = BoardInitializer.init_white_pieces_array()
        black_pieces = BoardInitializer.init_black_pieces_array()

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = black_pieces[index]
            index += 1

        index += 4 * BoardEnum.BOARD_LENGTH.value
        border_edge_index = 2 * BoardEnum.BOARD_LENGTH.value - 1

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = white_pieces[border_edge_index]
            border_edge_index -= 1
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

    def add_piece_to_the_board(self, piece: int, square: int) -> None:
        """
        Adds piece to board array and updates fen string.
        :param piece: int value of piece
        :param square: int index of where to add a piece
        :return: None
        """
        self.__board_array[square] = piece
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)

    def should_this_piece_move(self, row: int, col: int) -> bool:
        board_index = BoardEnum.BOARD_LENGTH.value * row + col
        color = ColorManager.get_piece_color(self.__board_array[board_index])

        return color == self.__color_to_move

    def is_it_legal_move(self, move: Move) -> bool:
        if move.get_moving_piece() in (PiecesEnum.BISHOP.value, PiecesEnum.ROOK.value, PiecesEnum.QUEEN.value):
            return move in self.__legal_moves
        return True
