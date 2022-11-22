from typing import Tuple

from numpy import array
from numpy import dtype
from numpy import int8
from numpy import ndarray

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.BoardInitializer import BoardInitializer
from game_window.board.BoardUtil import BoardUtil
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenFactory import FenFactory
from game_window.board.fen.FenMaker import FenMaker
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.MoveGenerator import MoveGenerator
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveList import MoveList


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders",
                       "__engine_color", "__player_color", "__fen_factory"], dtype=str)

    def __init__(self, fen_factory: FenFactory) -> None:
        self.__engine_color: int = PiecesEnum.BLACK.value
        self.__player_color: int = PiecesEnum.WHITE.value
        self.__board_array: ndarray[int, dtype[int8]] = BoardInitializer.init_starting_board(self.__engine_color,
                                                                                             self.__player_color)
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__fen_factory: FenFactory = fen_factory
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders: ndarray[int, dtype[int8]] = BoardUtil.calculate_distance_to_borders()
        self.__legal_moves: MoveList = MoveGenerator.generate_legal_moves(self.__color_to_move, self)

    def delete_piece_from_board_square(self, square: int) -> int:
        """
        Deletes piece_square from board and updates fen string.
        :param square:
        :return: deleted piece_square value
        """
        if square is None:
            raise NullArgumentException("SQUARE CANNOT BE NULL!")
        if square < 0 or square > 63:
            raise IllegalArgumentException("SQUARE CANNOT BE OVER THE BOUNDS OF BOARD!")

        piece: int = self.__board_array[square]
        self.__board_array[square] = 0
        self.update_fen()

        return piece

    def add_piece_to_the_board(self, piece: int, square: int) -> None:
        """
        Adds piece_square to board array and updates fen string.
        :param piece: int value of piece_square
        :param square: int index of where to add a piece_square
        :return: None
        """
        if piece is None or square is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULL ON ADDING!")
        if square < 0 or square > 63:
            raise IllegalArgumentException("SQUARE IS NOT WITHING THE BOARD BONDS!")
        piece_value: int = piece - ColorManager.get_piece_color(piece)

        if piece_value not in PiecesEnum.PIECES_TUPLE.value:
            raise IllegalArgumentException("SUCH PIECE DOES NOT EXIST")

        self.__board_array[square] = piece
        self.update_fen()

    def should_this_piece_move(self, row: int, col: int) -> bool:
        """
        Checks if piece_square on boards row and col indexes should move.
        :param row: int value of row index
        :param col: int value of col index
        :return: bool value if piece_square should move or not
        """
        if row is None or col is None:
            raise NullArgumentException("ROWS ANC COLS CANNOT BE NULLS!")

        if row < 0 or col < 0 or row > 7 or col > 7:
            raise IllegalArgumentException("ROWS ANC COLS CANNOT BE LESS THAN 0!")
        board_index: int = BoardEnum.BOARD_LENGTH.value * row + col

        return ColorManager.get_piece_color(self.__board_array[board_index]) == self.__color_to_move

    def update_legal_moves(self, color: int) -> None:
        """
        Method used to set legal moves_list list
        :param color: int value of color
        :return: None
        """
        self.__legal_moves = MoveGenerator.generate_legal_moves(color, self)

    def set_opposite_move_color(self) -> None:
        """
        Method used to change the color of players pieces which is turn.
        :return: None
        """
        self.__color_to_move = PiecesEnum.WHITE.value if self.__color_to_move == PiecesEnum.BLACK.value else PiecesEnum.BLACK.value

    def legal_moves(self) -> MoveList:
        """
        Gives access to legal moves_list list.
        :return: list of moves_list
        """
        return self.__legal_moves

    def distances(self) -> ndarray[int, dtype[int8]]:
        """
        Gives access to distances to borders array
        :return: ndarray of distances
        """
        return self.__distances_to_borders

    def board_array(self) -> ndarray[int, dtype[int8]]:
        """
        Gives access to board int array.
        :return: board int array
        """
        return self.__board_array

    def fen_string(self) -> str:
        """
        Gives access to the fen string.
        :return: fen string
        """
        return self.__fen_string

    def color_to_move(self) -> int:
        """
        Gives access to color which is turn to move
        :return: int value of color
        """
        return self.__color_to_move

    def is_it_legal_move(self, move: Move) -> bool:
        """
        Checks if move given can be played
        :param move: current move player wants to play
        :return: bool value whether move is legal or not
        """
        return move in self.__legal_moves

    def update_fen(self) -> None:
        """
        Method used to update fen string with current board state
        :return: None
        """
        self.__fen_string = self.__fen_factory.convert_board_array_to_fen(self)

    def disable_castling_if_captured_rook(self, deleted_piece, color, square) -> None:
        """
        Method used to disable castling if rook was captured
        :param deleted_piece: int value of deleted piece
        :param color: int value of friendly color
        :param square: int index of rook square
        :return: None
        """
        self.__fen_factory.disable_castling_if_captured_rook(deleted_piece, color, square, self)

    def switch_colors(self) -> None:
        """
        Method used to switch sides of board
        :return: None
        """
        self.set_opposite_color_sides()
        self.__board_array = BoardInitializer.init_starting_board(self.__engine_color, self.__player_color)
        self.__fen_factory: FenFactory = FenMaker(FenData(self.__player_color))
        self.__color_to_move = PiecesEnum.WHITE.value
        self.update_fen()
        self.__legal_moves = MoveGenerator.generate_legal_moves(self.__color_to_move, self)

    def set_opposite_color_sides(self) -> None:
        """
        Method used in board inversion to set opposite colors
        :return: None
        """
        self.__engine_color = ColorManager.get_opposite_piece_color(self.__engine_color)
        self.__player_color = ColorManager.get_opposite_piece_color(self.__player_color)

    def engine_color(self) -> int:
        """
        Method used to get access to engine color
        :return: int value of engine color
        """
        return self.__engine_color

    def player_color(self) -> int:
        """
        Method used to get access to player color
        :return: int value of player color
        """
        return self.__player_color

    def update_fen_data_with_double_pawn_movement(self, move: Move) -> None:
        """
        Method used to validate double pawn movement in terms of fen data
        :param move: Move instance
        :return None
        """
        self.__fen_factory.update_fen_data_with_double_pawn_movement(move)

    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        self.__fen_factory.set_castling_king_side(can_castle, color)

    def set_castling_queen_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on queen side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        self.__fen_factory.set_castling_queen_side(can_castle, color)

    def en_passant_square(self) -> int:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        return self.__fen_factory.en_passant_square()

    def en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant end_square value
        :return: int value of en passant square
        """
        return self.__fen_factory.en_passant_piece_square()

    def set_en_passant_piece_square(self, piece_square: int) -> None:
        """
        Gives access to an en passant piece end_square value
        :return: int value of an en passant target square
        """
        self.__fen_factory.set_en_passant_piece_square(piece_square)

    def set_en_passant_square(self, square: int) -> None:
        """
        Method used to set en passant end_square
        :param square: int value of end_square
        :return: None
        """
        self.__fen_factory.set_en_passant_square(square)

    def update_move_counter(self) -> None:
        """
        Increments move counter by 1
        :return: None
        """
        self.__fen_factory.update_move_counter()

    def can_king_castle_king_side(self, color: int) -> bool:
        """
        Returns if king can castle on king side
        :param color: int value of color
        :return: bool
        """
        return self.__fen_factory.can_king_castle_king_side(color)

    def can_king_castle_queen_side(self, color: int) -> bool:
        """
        Returns if king can castle on queen side
        :param color: int value of color
        :return: bool
        """
        return self.__fen_factory.can_king_castle_queen_side(color)

    def get_special_move_data(self) -> Tuple[bool, bool, bool, bool, int, int, int, int]:
        """
        Method used to return a tuple of special fen data for making and unmaking moves_list
        :return: tuple
        """
        return self.__fen_factory.get_special_move_data()

    def update_fen_data(self, prev_fen_data: MoveData) -> None:
        """
        Updates fen_data with move_data values
        :param prev_fen_data: MoveData instance
        :return: None
        """
        self.__fen_factory.update_fen_data(prev_fen_data)

    def update_no_sack_and_pawn_counter(self, deleted_piece: int, moving_piece: int) -> None:
        """
        Method used to update no sack and pawn move counter
        :param deleted_piece: int value of a piece
        :param moving_piece: int value of a moving piece
        :return: None
        """
        self.__fen_factory.update_no_sack_and_pawn_counter(deleted_piece, moving_piece)

    def disable_castling_on_side(self, color: int, target_square: int) -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :return: None
        """
        self.__fen_factory.disable_castling_on_side(color, target_square, self)
