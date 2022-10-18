from numpy import array
from numpy import ndarray
from numpy import sign

from game_window.BoardInitializer import BoardInitializer
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.FenData import FenData
from game_window.FenFactory import FenFactory
from game_window.moving.Move import Move
from game_window.moving.MoveGenerator import MoveGenerator
from game_window.moving.MoveList import MoveList
from game_window.moving.MoveValidator import MoveValidator


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders",
                       "__fen_data", "__engine_color", "__player_color"], dtype=str)

    def __init__(self):
        self.__engine_color: int = PiecesEnum.BLACK.value
        self.__player_color: int = PiecesEnum.WHITE.value
        self.__board_array: ndarray[int] = BoardInitializer.init_starting_board(self.__engine_color,
                                                                                self.__player_color)
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__fen_data: FenData = FenData(self.__player_color)
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders: ndarray[int] = MoveGenerator.calculate_distance_to_borders()
        self.__legal_moves: MoveList = MoveGenerator.generate_legal_moves(self.__color_to_move, self)

    def castle_king(self, piece: int, move: Move) -> None:
        """
        Method used to castle king it means prepare board for castling
        :param piece: int value of piece_square
        :param move: Move instance
        :return: None
        """
        start_square: int = move.get_start_square()
        end_square: int = move.get_end_square()
        distance: int = start_square - end_square
        color: int = ColorManager.get_piece_color(piece)
        is_queen_side: bool = distance > 0
        rook_position: int = MoveValidator.get_rook_position(color, is_queen_side, self.__engine_color,
                                                             self.__player_color)

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
        start_square: int = move.get_start_square()
        end_square: int = move.get_end_square()
        distance: int = start_square - end_square
        is_queen_side: bool = distance > 0
        rook_position: int = MoveValidator.get_rook_position(color, is_queen_side, self.__engine_color,
                                                             self.__player_color)

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

    def get_distances(self) -> ndarray[int]:
        """
        Gives access to distances to borders array
        :return: ndarray of distances
        """
        return self.__distances_to_borders

    def get_board_array(self) -> ndarray[int]:
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
        self.__board_array[square] = piece
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

    def should_this_piece_move(self, row: int, col: int) -> bool:
        """
        Checks if piece_square on boards row and col indexes should move.
        :param row: int value of row index
        :param col: int value of col index
        :return: bool value if piece_square should move or not
        """
        board_index: int = BoardEnum.BOARD_LENGTH.value * row + col

        return ColorManager.get_piece_color(self.__board_array[board_index]) == self.__color_to_move

    def is_it_legal_move(self, move: Move) -> bool:
        """
        Checks if move given can be played
        :param move: current move player wants to play
        :return: bool value whether move is legal or not
        """
        return move in self.__legal_moves.moves

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
        self.__fen_data.__init__(self.__player_color)
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

    def __eq__(self, other):
        if not isinstance(other, Board):
            return False
        if self.__board_array != other.get_board_array() or self.__player_color != other.get_player_color():
            return False
        if self.__engine_color != other.get_engine_color() or self.__fen_string != other.get_fen_string():
            return False
        if self.__fen_data != other.get_fen_data() or self.__legal_moves != other.get_legal_moves():
            return False
        return self.__distances_to_borders == other.get_distances() and self.__color_to_move == other.get_color_to_move()

    def __hash__(self):
        return hash((self.__color_to_move, self.__player_color, self.__engine_color, self.__distances_to_borders.tobytes(),
                     self.__board_array.tobytes(), self.__fen_string, self.__fen_data))
