from typing import TYPE_CHECKING
from typing import Tuple

from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.ColorManager import ColorManager
from src.main.game_window.board.fen.FenData import FenData
from src.main.game_window.board.fen.FenFactory import FenFactory
from src.main.game_window.board.fen.FenUtil import FenUtil
from src.main.game_window.enums.BoardEnum import BoardEnum
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.data.MoveData import MoveData

if TYPE_CHECKING:
    from src.main.game_window.board.Board import Board


class FenMaker(FenFactory):
    """
    Class containing methods to manage fen creation.
    """

    __slots__ = "__fen_data"

    def __init__(self, fen_data: FenData):
        self.__fen_data = fen_data

    def convert_board_array_to_fen(self, board: 'Board') -> str:
        """
        Method converts int array into fen string
        :param board: Board instance
        :return: fen string
        """
        fen = ""
        current_element = 0
        board_array = board.board_array()

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
        fen = f"{fen}{FenUtil.get_color_to_move_fen_letter(board.color_to_move())}"
        fen = f"{fen}{FenUtil.get_castling_letters_to_fen(self.__fen_data)}"
        fen = f"{fen}{FenUtil.convert_square_into_board_double_index(self.__fen_data.en_passant_square())}"
        fen = f"{fen} {self.__fen_data.get_no_sack_and_pawn_count()} {self.__fen_data.get_move_counter()}"

        return fen

    def update_no_sack_and_pawn_counter(self, deleted_piece: int, moving_piece: int) -> None:
        """
        Method used to update no sack and pawn move counter
        :param deleted_piece: int value of a piece
        :param moving_piece: int value of a moving piece
        :return: None
        """
        if deleted_piece is None or moving_piece is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if deleted_piece < 0 or moving_piece not in PiecesEnum.PIECES_TUPLE.value:
            raise IllegalArgumentException("IMPOSSIBLE ARGUMENTS GIVEN!")

        if deleted_piece != 0 or moving_piece == PiecesEnum.PAWN.value:
            self.__fen_data.update_no_sack_and_pawn_count(True)
        elif deleted_piece == 0 or moving_piece != PiecesEnum.PAWN.value:
            self.__fen_data.update_no_sack_and_pawn_count(False)

    def disable_castling_on_side(self, color: int, target_square: int, board: 'Board') -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        if board is None or color is None or target_square is None:
            raise NullArgumentException("METHOD ARGUMENTS CANNOT BE NULLS!")
        if target_square < 0 or target_square > 63 or not ColorManager.is_it_valid_color(color):
            raise IllegalArgumentException("ARGUMENTS ARE NOT WITHIN ACCEPTABLE BONDS!")

        if target_square in (MoveEnum.TOP_ROOK_QUEEN.value, MoveEnum.BOTTOM_ROOK_QUEEN.value):
            self.__fen_data.set_castling_queen_side(False, color)
        elif target_square in (MoveEnum.TOP_ROOK_KING.value, MoveEnum.BOTTOM_ROOK_KING.value):
            self.__fen_data.set_castling_king_side(False, color)

    def disable_castling_if_captured_rook(self, deleted_piece: int, color: int, square: int, board: 'Board') -> None:
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
        if square < 0 or square > 63 or not ColorManager.is_it_valid_color(color):
            raise IllegalArgumentException("WRONG PARAMETERS GIVEN!")
        enemy_color: int = ColorManager.get_opposite_piece_color(color)

        if deleted_piece == enemy_color | PiecesEnum.ROOK.value:
            self.disable_castling_on_side(enemy_color, square, board)

    def update_fen_data_with_double_pawn_movement(self, move: Move) -> None:
        """
        Method used to validate double pawn movement in terms of fen data
        :param move: Move instance
        :return None
        """
        end_square: int = move.get_end_square()
        moving_piece: int = move.get_moving_piece()
        move_length: int = end_square - move.get_start_square()

        if move_length == MoveEnum.PAWN_UP_DOUBLE_MOVE.value and moving_piece == PiecesEnum.PAWN.value:
            self.__fen_data.set_en_passant_square(end_square - MoveEnum.PAWN_UP_SINGLE_MOVE.value)
            self.__fen_data.set_en_passant_piece_square(end_square)

        elif move_length == MoveEnum.PAWN_DOWN_DOUBLE_MOVE.value and moving_piece == PiecesEnum.PAWN.value:
            self.__fen_data.set_en_passant_square(end_square - MoveEnum.PAWN_DOWN_SINGLE_MOVE.value)
            self.__fen_data.set_en_passant_piece_square(end_square)

        elif moving_piece != PiecesEnum.PAWN.value and self.__fen_data.en_passant_square() != -1:
            self.__fen_data.set_en_passant_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
            self.__fen_data.set_en_passant_piece_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)

    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        self.__fen_data.set_castling_king_side(can_castle, color)

    def set_castling_queen_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on queen side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        self.__fen_data.set_castling_queen_side(can_castle, color)

    def en_passant_square(self) -> int:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        return self.__fen_data.en_passant_square()

    def en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant end_square value
        :return: int value of en passant square
        """
        return self.__fen_data.en_passant_piece_square()

    def set_en_passant_piece_square(self, piece_square: int) -> None:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        self.__fen_data.set_en_passant_piece_square(piece_square)

    def set_en_passant_square(self, square: int) -> None:
        """
        Method used to set en passant end_square
        :param square: int value of end_square
        :return: None
        """
        self.__fen_data.set_en_passant_square(square)

    def update_move_counter(self) -> None:
        """
        Increments move counter by 1
        :return: None
        """
        self.__fen_data.update_move_counter()

    def can_king_castle_king_side(self, color: int) -> bool:
        """
        Returns if king can castle on king side
        :param color: int value of color
        :return: bool
        """
        return self.__fen_data.can_king_castle_king_side(color)

    def can_king_castle_queen_side(self, color: int) -> bool:
        """
        Returns if king can castle on queen side
        :param color: int value of color
        :return: bool
        """
        return self.__fen_data.can_king_castle_queen_side(color)

    def get_special_move_data(self) -> Tuple[bool, bool, bool, bool, int, int, int, int]:
        """
        Method used to return a tuple of special fen data for making and unmaking moves_list
        :return: tuple
        """
        return self.__fen_data.get_special_move_data()

    def update_fen_data(self, prev_fen_data: MoveData) -> None:
        """
        Updates fen_data with move_data values
        :param prev_fen_data: MoveData instance
        :return: None
        """
        self.__fen_data.update_fen_data(prev_fen_data)
