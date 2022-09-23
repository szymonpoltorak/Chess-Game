from numpy import ndarray

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class FenFactory:
    """
    Class containing methods to manage fen creation.
    """
    @staticmethod
    def convert_board_array_to_fen(board: ndarray[int]) -> str:
        """
        Method converts int array into fen string
        :param board: board int array
        :return: fen string
        """
        fen = ""
        current_element = 0

        for row in range(BoardEnum.BOARD_LENGTH.value):
            none_counter = 0

            for col in range(BoardEnum.BOARD_LENGTH.value):
                index = current_element + col
                color_value = FenFactory.get_proper_color_value(board[index])

                if board[index] == PiecesEnum.NONE.value:
                    none_counter += 1
                    continue
                if none_counter > 0:
                    fen += str(none_counter)
                    none_counter = 0
                fen += FenFactory.get_proper_piece_for_fen(board, index, color_value)
            if none_counter > 0:
                fen += str(none_counter)
            if row != 7:
                fen += "/"
            current_element += BoardEnum.BOARD_LENGTH.value
        fen += " w KQkq - 0 1" #TODO generate last part of fen

        return fen

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
    def get_proper_fen_character(color_value: int, letter: str):
        """
        Returns proper fen characters based on color value.
        :param color_value: int value of piece_square color
        :param letter: str representation of piece_square
        :return: proper fen str letter
        """
        if color_value == PiecesEnum.WHITE.value:
            return letter.upper()
        return letter

    @staticmethod
    def get_proper_piece_for_fen(board: ndarray[int], index: int, color_value: int) -> str:
        """
        Gets proper fen letter for board int array.
        :param board: int array of board
        :param index: index of current position in board
        :param color_value: int value of color
        :return: proper str letter
        """
        if board[index] == color_value | PiecesEnum.PAWN.value:
            return FenFactory.get_proper_fen_character(color_value, "p")
        elif board[index] == color_value | PiecesEnum.KING.value:
            return FenFactory.get_proper_fen_character(color_value, "k")
        elif board[index] == color_value | PiecesEnum.QUEEN.value:
            return FenFactory.get_proper_fen_character(color_value, "q")
        elif board[index] == color_value | PiecesEnum.BISHOP.value:
            return FenFactory.get_proper_fen_character(color_value, "b")
        elif board[index] == color_value | PiecesEnum.KNIGHT.value:
            return FenFactory.get_proper_fen_character(color_value, "n")
        elif board[index] == color_value | PiecesEnum.ROOK.value:
            return FenFactory.get_proper_fen_character(color_value, "r")
