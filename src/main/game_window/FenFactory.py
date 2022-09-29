from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.Board import Board


class FenFactory:
    """
    Class containing methods to manage fen creation.
    """
    @staticmethod
    def convert_board_array_to_fen(board: 'Board') -> str:
        """
        Method converts int array into fen string
        :param board: Board instance
        :return: fen string
        """
        fen = ""
        current_element = 0
        board_array = board.get_board_array()

        for row in range(BoardEnum.BOARD_LENGTH.value):
            none_counter = 0

            for col in range(BoardEnum.BOARD_LENGTH.value):
                index = current_element + col
                color_value = FenFactory.get_proper_color_value(board_array[index])

                if board_array[index] == PiecesEnum.NONE.value:
                    none_counter += 1
                    continue
                if none_counter > 0:
                    fen += str(none_counter)
                    none_counter = 0
                fen += FenFactory.get_proper_piece_for_fen(board_array, index, color_value)
            if none_counter > 0:
                fen += str(none_counter)
            if row != 7:
                fen += "/"
            current_element += BoardEnum.BOARD_LENGTH.value
        fen += FenFactory.get_color_to_move_fen_letter(board.get_color_to_move())
        fen += FenFactory.add_castling_letters_to_fen(board)
        fen += FenFactory.convert_square_into_board_double_index(board.get_fen_data().get_en_passant_square())
        fen += f" {board.get_fen_data().get_no_sack_and_pawn_count()}"
        fen += f" {board.get_fen_data().get_move_counter()}"

        return fen

    @staticmethod
    def convert_square_into_board_double_index(square: int) -> str:
        """
        Method to convert square board index into chess board index
        :param square: int value of square
        :return: str
        """
        if square == -1:
            return " -"

        col = square % BoardEnum.BOARD_LENGTH.value
        row = BoardEnum.BOARD_LENGTH.value - int((square - col) / BoardEnum.BOARD_LENGTH.value)
        cols = array(["a", "b", "c", "d", "e", "f", "g", "h"])

        return f" {cols[col]}{row}"

    @staticmethod
    def get_color_to_move_fen_letter(color: int) -> str:
        """
        Method returns a letter of current to move color
        :param color: int value of color
        :return: str
        """
        if color == PiecesEnum.WHITE.value:
            return " w"
        return " b"

    @staticmethod
    def get_proper_letter_size(color: int, letter: str) -> str:
        """
        Method returns proper case of letter (upper of lower) for fen
        :param color: int value of color
        :param letter: str
        :return: str
        """
        if color == PiecesEnum.WHITE.value:
            return letter.upper()
        return letter

    @staticmethod
    def add_castling_letters_to_fen(board: 'Board') -> str:
        """
        Method to get proper letters representing castling capabilities of kings
        :param board: Board instance
        :return: str
        """
        castle_string = " "

        if board.get_fen_data().can_king_castle_king_side(PiecesEnum.WHITE.value):
            castle_string += FenFactory.get_proper_letter_size(PiecesEnum.WHITE.value, "k")
        if board.get_fen_data().can_king_castle_queen_side(PiecesEnum.WHITE.value):
            castle_string += FenFactory.get_proper_letter_size(PiecesEnum.WHITE.value, "q")
        if board.get_fen_data().can_king_castle_queen_side(PiecesEnum.BLACK.value):
            castle_string += FenFactory.get_proper_letter_size(PiecesEnum.BLACK.value, "k")
        if board.get_fen_data().can_king_castle_queen_side(PiecesEnum.BLACK.value):
            castle_string += FenFactory.get_proper_letter_size(PiecesEnum.BLACK.value, "q")
        if castle_string == " ":
            return " -"
        return castle_string

    @staticmethod
    def get_proper_color_value(piece_value: int) -> int:
        """
        Gives proper color value based on piece_square value.
        :param piece_value: int piece_square value
        :return: piece_square color value
        """
        white = PiecesEnum.WHITE.value
        black = PiecesEnum.BLACK.value

        if piece_value - black < 0:
            return white
        return black

    @staticmethod
    def get_proper_piece_for_fen(board: ndarray[int], index: int, color_value: int) -> str:
        """
        Gets proper fen letter for board int array.
        :param board: int array of board
        :param index: index of current position in board
        :param color_value: int value of color
        :return: proper str letter
        """
        piece = board[index]
        if piece == color_value | PiecesEnum.PAWN.value:
            return FenFactory.get_proper_letter_size(color_value, "p")
        elif piece == color_value | PiecesEnum.KING.value:
            return FenFactory.get_proper_letter_size(color_value, "k")
        elif piece == color_value | PiecesEnum.QUEEN.value:
            return FenFactory.get_proper_letter_size(color_value, "q")
        elif piece == color_value | PiecesEnum.BISHOP.value:
            return FenFactory.get_proper_letter_size(color_value, "b")
        elif piece == color_value | PiecesEnum.KNIGHT.value:
            return FenFactory.get_proper_letter_size(color_value, "n")
        elif piece == color_value | PiecesEnum.ROOK.value:
            return FenFactory.get_proper_letter_size(color_value, "r")
