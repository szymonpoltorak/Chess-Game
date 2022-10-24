from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.board.fen.FenData import FenData
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class FenUtil:
    """
    Class containing fen util methods for managing fen and its dependencies
    """

    @staticmethod
    def update_no_sack_and_pawn_counter(fen_data: FenData, deleted_piece: int, moving_piece: int) -> None:
        """
        Method used to update no sack and pawn move counter
        :param fen_data: FenData instance
        :param deleted_piece: int value of a piece
        :param moving_piece: int value of a moving piece
        :return: None
        """
        if deleted_piece != 0 or moving_piece == PiecesEnum.PAWN.value:
            fen_data.update_no_sack_and_pawn_count(True)
        elif deleted_piece == 0 or moving_piece != PiecesEnum.PAWN.value:
            fen_data.update_no_sack_and_pawn_count(False)
        else:
            raise ValueError("NOT POSSIBLE CONDITION OCCURRED! WRONG PARAMETERS")

    @staticmethod
    def disable_castling_on_side(color: int, target_square: int, board: 'Board') -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        fen_data: FenData = board.get_fen_data()

        if target_square in (MoveEnum.TOP_ROOK_QUEEN.value, MoveEnum.BOTTOM_ROOK_QUEEN.value):
            fen_data.set_castling_queen_side(False, color)
        elif target_square in (MoveEnum.TOP_ROOK_KING.value, MoveEnum.BOTTOM_ROOK_KING.value):
            fen_data.set_castling_king_side(False, color)

    @staticmethod
    def disable_castling_if_deleted_rook(deleted_piece: int, color: int, square: int, board: 'Board') -> None:
        """
        Method used to disable castling if rook was captured
        :param deleted_piece: int value of deleted piece
        :param color: int value of friendly color
        :param square: int index of rook square
        :param board: Board instance
        :return: None
        """
        if deleted_piece == ColorManager.get_opposite_piece_color(color) | PiecesEnum.ROOK.value:
            FenUtil.disable_castling_on_side(ColorManager.get_opposite_piece_color(color), square, board)

    @staticmethod
    def convert_square_into_board_double_index(square: int) -> str:
        """
        Method to convert end_square board index into chess board index
        :param square: int value of end_square
        :return: str
        """
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
        return " w" if color == PiecesEnum.WHITE.value else " b"

    @staticmethod
    def get_proper_letter_size(color: int, letter: str) -> str:
        """
        Method returns proper case of letter (upper of lower) for fen
        :param color: int value of color
        :param letter: str
        :return: str
        """
        return letter.upper() if color == PiecesEnum.WHITE.value else letter

    @staticmethod
    def add_castling_letters_to_fen(board: 'Board') -> str:
        """
        Method to get proper letters representing castling capabilities of kings
        :param board: Board instance
        :return: str
        """
        fen_data = board.get_fen_data()
        king = "k"
        queen = "q"
        castle_string = " "

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
    def get_proper_color_value(piece_value: int) -> int:
        """
        Gives proper color value based on piece_square value.
        :param piece_value: int piece_square value
        :return: piece_square color value
        """
        return PiecesEnum.WHITE.value if piece_value - PiecesEnum.BLACK.value < 0 else PiecesEnum.BLACK.value

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
        piece_letters = {
            color_value | PiecesEnum.PAWN.value: "p",
            color_value | PiecesEnum.KING.value: "k",
            color_value | PiecesEnum.QUEEN.value: "q",
            color_value | PiecesEnum.BISHOP.value: "b",
            color_value | PiecesEnum.KNIGHT.value: "n",
            color_value | PiecesEnum.ROOK.value: "r"
        }
        return FenUtil.get_proper_letter_size(color_value, piece_letters[piece])
