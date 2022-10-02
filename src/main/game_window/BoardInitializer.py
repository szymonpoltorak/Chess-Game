from numpy import array
from numpy import ndarray
from numpy import zeros

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class BoardInitializer:
    @staticmethod
    def init_black_pieces_array() -> ndarray[int]:
        """
        Initializes array of pieces on starting position depending on given color value.
        :return: array of starting pieces of given color
        """
        piece_array = array([PiecesEnum.BLACK.value | PiecesEnum.ROOK.value,
                             PiecesEnum.BLACK.value | PiecesEnum.KNIGHT.value,
                             PiecesEnum.BLACK.value | PiecesEnum.BISHOP.value,
                             PiecesEnum.BLACK.value | PiecesEnum.QUEEN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.KING.value,
                             PiecesEnum.BLACK.value | PiecesEnum.BISHOP.value,
                             PiecesEnum.BLACK.value | PiecesEnum.KNIGHT.value,
                             PiecesEnum.BLACK.value | PiecesEnum.ROOK.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value])
        return piece_array

    @staticmethod
    def init_white_pieces_array() -> ndarray[int]:
        """
        Initializes array of pieces on starting position depending on given color value.
        :return: array of starting pieces of given color
        """
        return array([PiecesEnum.WHITE.value | PiecesEnum.ROOK.value,
                      PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value,
                      PiecesEnum.WHITE.value | PiecesEnum.BISHOP.value,
                      PiecesEnum.WHITE.value | PiecesEnum.KING.value,
                      PiecesEnum.WHITE.value | PiecesEnum.QUEEN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.BISHOP.value,
                      PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value,
                      PiecesEnum.WHITE.value | PiecesEnum.ROOK.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value])

    @staticmethod
    def init_starting_board(upper_color: int, down_color: int) -> ndarray[int]:
        """
        Method initializes starting board.
        :return: board int array
        """
        board = zeros(BoardEnum.BOARD_SIZE.value)
        index = 0
        upper_pieces = BoardInitializer.get_proper_pieces_arrays(upper_color)
        down_pieces = BoardInitializer.get_proper_pieces_arrays(down_color)

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = upper_pieces[index]
            index += 1

        index += 4 * BoardEnum.BOARD_LENGTH.value
        border_edge_index = 2 * BoardEnum.BOARD_LENGTH.value - 1

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = down_pieces[border_edge_index]
            border_edge_index -= 1
            index += 1
        return board

    @staticmethod
    def get_proper_pieces_arrays(color: int):
        if color == PiecesEnum.WHITE.value:
            return BoardInitializer.init_white_pieces_array()
        return BoardInitializer.init_black_pieces_array()
