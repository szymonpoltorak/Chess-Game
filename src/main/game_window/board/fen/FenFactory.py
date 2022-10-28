from typing import TYPE_CHECKING

from game_window.board.fen.FenUtil import FenUtil
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class FenFactory:
    """
    Class containing methods to manage fen creation.
    """
    __slots__ = ()

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
                color_value = ColorManager.get_piece_color(board_array[index])

                if board_array[index] == PiecesEnum.NONE.value:
                    none_counter += 1
                    continue
                if none_counter > 0:
                    fen = f"{fen}{none_counter}"
                    none_counter = 0
                fen = f"{fen}{FenUtil.get_proper_piece_for_fen(board_array, index, color_value)}"
            if none_counter > 0:
                fen = f"{fen}{none_counter}"
            if row != 7:
                fen = f"{fen}/"
            current_element += BoardEnum.BOARD_LENGTH.value
        fen = f"{fen}{FenUtil.get_color_to_move_fen_letter(board.get_color_to_move())}"
        fen = f"{fen}{FenUtil.add_castling_letters_to_fen(board.get_fen_data())}"
        fen = f"{fen}{FenUtil.convert_square_into_board_double_index(board.get_fen_data().get_en_passant_square())}"
        fen = f"{fen} {board.get_fen_data().get_no_sack_and_pawn_count()} {board.get_fen_data().get_move_counter()}"

        return fen
