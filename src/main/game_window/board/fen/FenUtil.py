from numpy import array
from numpy import dtype
from numpy import int8
from numpy._typing import NDArray

from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.ColorManager import ColorManager
from src.main.game_window.board.fen.FenData import FenData
from src.main.game_window.enums.BoardEnum import BoardEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum


class FenUtil:
    """
    Class containing fen util methods for managing fen and its dependencies
    """

    @staticmethod
    def convert_square_into_board_double_index(square: int) -> str:
        """
        Method to convert end_square board index into chess board index
        :param square: int value of end_square
        :return: str
        """
        if square is None:
            raise NullArgumentException("SQUARE CANNOT BE NULL!")
        if square < -1 or square > 63:
            raise IllegalArgumentException("SQUARE IS NOT WITHIN ACCEPTABLE BONDS!")
        if square == -1:
            return " -"

        col: int = square % BoardEnum.BOARD_LENGTH.value
        row: int = BoardEnum.BOARD_LENGTH.value - int((square - col) / BoardEnum.BOARD_LENGTH.value)
        cols = array(["a", "b", "c", "d", "e", "f", "g", "h"])

        return f" {cols[col]}{row}"

    @staticmethod
    def get_color_to_move_fen_letter(color: int) -> str:
        """
        Method returns a letter of current to move color
        :param color: int value of color
        :return: str
        """
        if color is None:
            raise NullArgumentException("COLOR CANNOT BE NULL!")
        if color not in (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value):
            raise IllegalArgumentException("SUCH COLOR DOES NOT EXIST!")
        return " w" if color == PiecesEnum.WHITE.value else " b"

    @staticmethod
    def get_proper_letter_size(color: int, letter: str) -> str:
        """
        Method returns proper case of letter (upper of lower) for fen
        :param color: int value of color
        :param letter: str
        :return: str
        """
        if color is None or letter is None:
            raise NullArgumentException("COLOR AND LETTER CANNOT BE NULLS!")
        if not ColorManager.is_it_valid_color(color):
            raise IllegalArgumentException("SUCH COLOR DOES NOT EXIST!")
        return letter.upper() if color == PiecesEnum.WHITE.value else letter

    @staticmethod
    def get_castling_letters_to_fen(fen_data: FenData) -> str:
        """
        Method to get proper letters representing castling capabilities of kings
        :param fen_data: FenData instance
        :return: str
        """
        if fen_data is None:
            raise NullArgumentException("FEN DATA CANNOT BE NULL!")
        king: str = "k"
        queen: str = "q"
        castle_string: str = " "

        if fen_data.can_king_castle_king_side(PiecesEnum.WHITE.value):
            castle_string = f"{castle_string}{FenUtil.get_proper_letter_size(PiecesEnum.WHITE.value, king)}"
        if fen_data.can_king_castle_queen_side(PiecesEnum.WHITE.value):
            castle_string = f"{castle_string}{FenUtil.get_proper_letter_size(PiecesEnum.WHITE.value, queen)}"
        if fen_data.can_king_castle_queen_side(PiecesEnum.BLACK.value):
            castle_string = f"{castle_string}{FenUtil.get_proper_letter_size(PiecesEnum.BLACK.value, king)}"
        if fen_data.can_king_castle_queen_side(PiecesEnum.BLACK.value):
            castle_string = f"{castle_string}{FenUtil.get_proper_letter_size(PiecesEnum.BLACK.value, queen)}"
        if castle_string == " ":
            return " -"
        return castle_string

    @staticmethod
    def get_proper_piece_for_fen(board: NDArray[int], index: int, color_value: int) -> str:
        """
        Gets proper fen letter for board int array.
        :param board: int array of board
        :param index: index of current position in board
        :param color_value: int value of color
        :return: proper str letter
        """
        if board is None or None in (board.any(), index, color_value):
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if index < 0 or index > 63 or not ColorManager.is_it_valid_color(color_value):
            raise IllegalArgumentException("ARGUMENTS ARE WITHIN NORMAL BONDS!")

        piece = board[index]
        piece_letters = {
            color_value | PiecesEnum.PAWN.value: "p",
            color_value | PiecesEnum.KING.value: "k",
            color_value | PiecesEnum.QUEEN.value: "q",
            color_value | PiecesEnum.BISHOP.value: "b",
            color_value | PiecesEnum.KNIGHT.value: "n",
            color_value | PiecesEnum.ROOK.value: "r"
        }
        return FenUtil.get_proper_letter_size(color_value, piece_letters[piece])
