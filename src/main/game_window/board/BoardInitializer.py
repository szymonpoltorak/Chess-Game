from numpy import array
from numpy import int8
from numpy import ndarray
from numpy import zeros

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class BoardInitializer:
    """
    Class used to initialize Board array
    """
    __slots__ = ()

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
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value], dtype=int8)
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
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value], dtype=int8)

    @staticmethod
    def init_starting_board(upper_color: int, down_color: int) -> ndarray[int]:
        """
        Method initializes starting board.
        :return: board int array
        """
        board: ndarray[int] = zeros(BoardEnum.BOARD_SIZE.value, dtype=int8)
        index: int = 0
        engine_pieces: ndarray[int] = BoardInitializer.get_proper_pieces_arrays(upper_color)
        player_pieces: ndarray[int] = BoardInitializer.get_proper_pieces_arrays(down_color)

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = engine_pieces[index]
            index += 1

        index += 4 * BoardEnum.BOARD_LENGTH.value
        border_edge_index = 2 * BoardEnum.BOARD_LENGTH.value - 1

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = player_pieces[border_edge_index]
            border_edge_index -= 1
            index += 1
        return board

    @staticmethod
    def get_proper_pieces_arrays(color: int) -> ndarray[int]:
        """
        Method used to init proper color array
        :param color: int value of color
        :return: array containing proper color pieces
        """
        return BoardInitializer.init_white_pieces_array() if color == PiecesEnum.WHITE.value else \
            BoardInitializer.init_black_pieces_array()
