from typing import TYPE_CHECKING

from numpy import array
from numpy import ndarray

from game_window.board.fen.FenData import FenData
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.exceptions.IllegalArgumentException import IllegalArgumentException
from game_window.exceptions.IllegalStateException import IllegalStateException
from game_window.exceptions.NullArgumentException import NullArgumentException

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
        if deleted_piece is None or fen_data is None or moving_piece is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if deleted_piece < 0 or moving_piece not in PiecesEnum.PIECES_TUPLE.value:
            raise IllegalArgumentException("IMPOSSIBLE ARGUMENTS GIVEN!")

        if deleted_piece != 0 or moving_piece == PiecesEnum.PAWN.value:
            fen_data.update_no_sack_and_pawn_count(True)
        elif deleted_piece == 0 or moving_piece != PiecesEnum.PAWN.value:
            fen_data.update_no_sack_and_pawn_count(False)
        else:
            raise IllegalStateException("NOT POSSIBLE CONDITION OCCURRED! WRONG PARAMETERS")

    @staticmethod
    def disable_castling_on_side(color: int, target_square: int, board: 'Board') -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        if board is None or color is None or target_square is None:
            raise NullArgumentException("METHOD ARGUMENTS CANNOT BE NULLS!")
        if target_square < 0 or target_square > 63 or color not in (PiecesEnum.WHITE.value, PiecesEnum.BLACK.value):
            raise IllegalArgumentException("ARGUMENTS ARE NOT WITHIN ACCEPTABLE BONDS!")

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
        if deleted_piece is None or color is None or square is None or board is None:
            raise NullArgumentException("GIVEN ARGUMENTS CANNOT BE NULLS!")
        if square < 0 or square > 63 or color not in (PiecesEnum.WHITE.value, PiecesEnum.BLACK.value):
            raise IllegalArgumentException("WRONG PARAMETERS GIVEN!")
        enemy_color: int = ColorManager.get_opposite_piece_color(color)

        if deleted_piece not in (enemy_color | 0, enemy_color | 1, enemy_color | 2, enemy_color | 3,
                                 enemy_color | 4, enemy_color | 5, enemy_color | 6):
            raise IllegalArgumentException("WRONG PARAMETERS GIVEN!")

        if deleted_piece == enemy_color | PiecesEnum.ROOK.value:
            FenUtil.disable_castling_on_side(enemy_color, square, board)

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
        if color not in (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value):
            raise IllegalArgumentException("SUCH COLOR DOES NOT EXIST!")
        return letter.upper() if color == PiecesEnum.WHITE.value else letter

    @staticmethod
    def add_castling_letters_to_fen(fen_data: FenData) -> str:
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
    def get_proper_piece_for_fen(board: ndarray[int], index: int, color_value: int) -> str:
        """
        Gets proper fen letter for board int array.
        :param board: int array of board
        :param index: index of current position in board
        :param color_value: int value of color
        :return: proper str letter
        """
        if board is None or None in (board.any(), index, color_value):
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if index < 0 or index > 63 or color_value not in (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value):
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
