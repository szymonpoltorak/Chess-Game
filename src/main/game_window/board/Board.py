from numpy import array, int8, dtype
from numpy import ndarray
from numpy import sign

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.ColorManager import ColorManager
from game_window.board.BoardInitializer import BoardInitializer
from game_window.board.BoardUtil import BoardUtil
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenFactory import FenFactory
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveList import MoveList
from game_window.moving.generation.MoveGenerator import MoveGenerator
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders",
                       "__fen_data", "__engine_color", "__player_color"], dtype=str)

    def __init__(self) -> None:
        self.__engine_color: int = PiecesEnum.BLACK.value
        self.__player_color: int = PiecesEnum.WHITE.value
        self.__board_array: ndarray[int, dtype[int8]] = BoardInitializer.init_starting_board(self.__engine_color,
                                                                                self.__player_color)
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__fen_data: FenData = FenData(self.__player_color)
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders: ndarray[int, dtype[int8]] = BoardUtil.calculate_distance_to_borders()
        self.__legal_moves: MoveList = MoveGenerator.generate_legal_moves(self.__color_to_move, self)

    def castle_king(self, piece: int, move: Move) -> None:
        """
        Method used to castle king it means prepare board for castling
        :param piece: int value of piece_square
        :param move: Move instance
        :return: None
        """
        if piece is None or move is None:
            raise NullArgumentException("METHODS ARGUMENTS CANNOT BE NULLS!")
        color: int = ColorManager.get_piece_color(piece)
        piece_value = piece - color

        if piece_value != PiecesEnum.KING.value:
            raise IllegalArgumentException("YOU CANNOT CASTLE PIECE WHICH IS NOT KING!")
        if move.get_special_flag_value() != SpecialFlags.CASTLING.value:
            raise IllegalArgumentException("THIS IS NOT CASTLING MOVE!")

        start_square: int = move.get_start_square()
        end_square: int = move.get_end_square()
        distance: int = start_square - end_square
        is_queen_side: bool = distance > 0
        rook_position: int = KingUtil.get_rook_position(color, is_queen_side, self.__engine_color, self.__player_color)

        self.__board_array[start_square] = PiecesEnum.NONE.value
        self.__board_array[end_square] = piece
        self.__board_array[rook_position] = PiecesEnum.NONE.value
        self.__board_array[end_square + sign(distance)] = color | PiecesEnum.ROOK.value

        self.__fen_data.set_castling_king_side(False, color)
        self.__fen_data.set_castling_queen_side(False, color)

    def un_castle_king(self, move: Move, color: int) -> None:
        """
        Method used to un castle king of given color
        :param move: Move which king made
        :param color: color value of a king
        :return: None
        """
        if move is None or color is None:
            raise NullArgumentException("MOVE AND COLOR CANNOT BE NULLS!")
        if move.get_special_flag_value() != SpecialFlags.CASTLING.value:
            raise IllegalArgumentException("IT IS NOT CASTLING MOVE!")
        if color not in (PiecesEnum.WHITE.value, PiecesEnum.BLACK.value):
            raise IllegalArgumentException("SUCH COLOR NOT EXISTS!")

        start_square: int = move.get_start_square()
        end_square: int = move.get_end_square()
        distance: int = start_square - end_square
        is_queen_side: bool = distance > 0
        rook_position: int = KingUtil.get_rook_position(color, is_queen_side, self.__engine_color, self.__player_color)

        self.__board_array[rook_position] = color | PiecesEnum.ROOK.value
        self.__board_array[move.get_end_square()] = PiecesEnum.NONE.value
        self.__board_array[end_square + sign(distance)] = PiecesEnum.NONE.value
        self.__board_array[move.get_start_square()] = color | PiecesEnum.KING.value

    def set_legal_moves(self, legal_moves: MoveList) -> None:
        """
        Method used to set legal moves_list list
        :param legal_moves: list of legal moves_list
        :return: None
        """
        self.__legal_moves = legal_moves

    def set_opposite_move_color(self) -> None:
        """
        Method used to change the color of players pieces which is turn.
        :return: None
        """
        self.__color_to_move = PiecesEnum.WHITE.value if self.__color_to_move == PiecesEnum.BLACK.value else PiecesEnum.BLACK.value

    def get_legal_moves(self) -> MoveList:
        """
        Gives access to legal moves_list list.
        :return: list of moves_list
        """
        return self.__legal_moves

    def get_distances(self) -> ndarray[int, dtype[int8]]:
        """
        Gives access to distances to borders array
        :return: ndarray of distances
        """
        return self.__distances_to_borders

    def get_board_array(self) -> ndarray[int, dtype[int8]]:
        """
        Gives access to board int array.
        :return: board int array
        """
        return self.__board_array

    def get_fen_string(self) -> str:
        """
        Gives access to the fen string.
        :return: fen string
        """
        return self.__fen_string

    def get_color_to_move(self) -> int:
        """
        Gives access to color which is turn to move
        :return: int value of color
        """
        return self.__color_to_move

    def delete_piece_from_board(self, row: int, col: int) -> int:
        """
        Deletes piece_square from board and updates fen string.
        :param row: row int index
        :param col: col int index
        :return: deleted piece_square value
        """
        if row is None or col is None:
            raise NullArgumentException("ROWS ANC COLS CANNOT BE NULLS!")
        if row < 0 or col < 0 or row > 7 or col > 7:
            raise IllegalArgumentException("ROWS ANC COLS CANNOT BE OVER THE BOUNDS OF BOARD!")

        board_index: int = BoardEnum.BOARD_LENGTH.value * row + col

        piece: int = self.__board_array[board_index]
        self.__board_array[board_index] = 0
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

        return piece

    def delete_pieces_on_squares(self, start_square: int, end_square: int) -> int:
        """
        Deletes pieces on squares in computer move
        :param start_square: a starting square of a moving piece index
        :param end_square: board array index
        :return: deleted piece_square value
        """
        if start_square is None or end_square is None:
            raise NullArgumentException("SQUARES CANNOT BE NULLS!")
        if start_square < 0 or start_square > 63:
            raise IllegalArgumentException("START SQUARE IS NOT WITHING BONDS!")
        if end_square < 0 or end_square > 63:
            raise IllegalArgumentException("START SQUARE IS NOT WITHING BONDS!")

        piece: int = self.__board_array[end_square]
        self.__board_array[end_square], self.__board_array[start_square] = 0, 0
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

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
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

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
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

    def make_en_passant_capture(self, piece: int) -> None:
        """
        Method used to make an en passant capture on board array
        :param piece: int value of piece
        :return: None
        """
        piece_value: int = piece - ColorManager.get_piece_color(piece)

        if piece_value != PiecesEnum.PAWN.value:
            raise IllegalArgumentException("THIS PIECE CANNOT MAKE AN EN PASSANT CAPTURE!")
        if piece is None:
            raise NullArgumentException("PIECE CANNOT BE NULL!")
        self.__board_array[self.__fen_data.get_en_passant_square()] = piece
        self.__board_array[self.__fen_data.get_en_passant_piece_square()] = 0

        self.__fen_data.set_en_passant_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
        self.__fen_data.set_en_passant_piece_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

    def switch_colors(self) -> None:
        """
        Method used to switch sides of board
        :return: None
        """
        self.set_opposite_color_sides()
        self.__board_array = BoardInitializer.init_starting_board(self.__engine_color, self.__player_color)
        self.__fen_data = FenData(self.__player_color)
        self.__color_to_move = PiecesEnum.WHITE.value
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)
        self.__legal_moves = MoveGenerator.generate_legal_moves(self.__color_to_move, self)

    def get_fen_data(self) -> FenData:
        """
        Gives access to the fen data field.
        :return: FenData instance
        """
        return self.__fen_data

    def set_opposite_color_sides(self) -> None:
        """
        Method used in board inversion to set opposite colors
        :return: None
        """
        self.__engine_color = ColorManager.get_opposite_piece_color(self.__engine_color)
        self.__player_color = ColorManager.get_opposite_piece_color(self.__player_color)

    def get_engine_color(self) -> int:
        """
        Method used to get access to engine color
        :return: int value of engine color
        """
        return self.__engine_color

    def get_player_color(self) -> int:
        """
        Method used to get access to player color
        :return: int value of player color
        """
        return self.__player_color

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False
        if self.__board_array != other.get_board_array() or self.__player_color != other.get_player_color():
            return False
        if self.__engine_color != other.get_engine_color() or self.__fen_string != other.get_fen_string():
            return False
        if self.__fen_data != other.get_fen_data() or self.__legal_moves != other.get_legal_moves():
            return False
        return self.__distances_to_borders == other.get_distances() and self.__color_to_move == other.get_color_to_move()

    def __hash__(self) -> int:
        return hash(
            (self.__color_to_move, self.__player_color, self.__engine_color, self.__distances_to_borders.tobytes(),
             self.__board_array.tobytes(), self.__fen_string, self.__fen_data))
