from numpy import ndarray

from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class FenFactory:
    @staticmethod
    def convert_board_array_to_fen(board: ndarray[int]) -> str:
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
                else:
                    fen += str(none_counter)
                    none_counter = 0
                fen += FenFactory.add_proper_piece_to_fen(board, index, color_value)
            if none_counter > 0:
                fen += str(none_counter)
            if row != 7:
                fen += "/"
            current_element += BoardEnum.BOARD_LENGTH.value
        fen += " w KQkq - 0 1" #TODO generate last part of fen

        return fen

    @staticmethod
    def get_proper_color_value(piece_value: int) -> int:
        white = PiecesEnum.WHITE.value
        black = PiecesEnum.BLACK.value

        if piece_value - black < 0:
            return white
        return black

    @staticmethod
    def get_proper_fen_character(color_value: int, letter: str):
        if color_value == PiecesEnum.WHITE.value:
            return letter.upper()
        return letter

    @staticmethod
    def add_proper_piece_to_fen(board: ndarray[int], index: int, color_value: int) -> str:
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
