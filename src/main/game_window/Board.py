from numpy import array
from numpy import ndarray
from numpy import zeros

from game_window.BoardInitializer import BoardInitializer
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.FenFactory import FenFactory
from game_window.Move import Move
from game_window.MoveGenerator import MoveGenerator
from game_window.MoveValidator import MoveValidator


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders",
                       "__white_castle_king", "__white_castle_queen",  "__black_castle_king", "__black_castle_queen",
                       "__en_passant_square", "__en_passant_piece_square", "__move_counter",
                       "__no_sack_and_pawn_count"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__white_castle_king = True
        self.__white_castle_queen = True
        self.__black_castle_king = True
        self.__black_castle_queen = True
        self.__en_passant_square = -1
        self.__en_passant_piece_square = -1
        self.__move_counter = 1
        self.__no_sack_and_pawn_count = 0
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders = MoveGenerator.calculate_distance_to_borders()
        self.__legal_moves = MoveGenerator.generate_legal_moves(self.__color_to_move, self)

    def can_king_castle_king_side(self, color: int) -> bool:
        """
        Returns if king can castle on king side
        :param color: int value of color
        :return: bool
        """
        if color == PiecesEnum.WHITE.value:
            return self.__white_castle_king
        else:
            return self.__black_castle_king

    def can_king_castle_queen_side(self, color: int) -> bool:
        """
        Returns if king can castle on queen side
        :param color: int value of color
        :return: bool
        """
        if color == PiecesEnum.WHITE.value:
            return self.__white_castle_queen
        else:
            return self.__black_castle_queen

    def set_castling_king_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on king side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        if color == PiecesEnum.WHITE.value:
            self.__white_castle_king = can_castle
        else:
            self.__black_castle_king = can_castle

    def update_move_counter(self) -> None:
        """
        Increments move counter by 1
        :return: None
        """
        self.__move_counter += 1

    def get_move_counter(self) -> int:
        """
        Gives access to move counter current value
        :return: int value of counter
        """
        return self.__move_counter

    def get_no_sack_and_pawn_count(self) -> int:
        """
        Gives access to counter of how many moves have passed since last pawn move or any sack
        :return: int value of counter
        """
        return self.__no_sack_and_pawn_count

    def update_no_sack_and_pawn_count(self, to_zero: bool) -> None:
        """
        Updates no sack and no pawn move counter or makes it equal to 0
        :param to_zero: bool value if counter should be made 0 or not
        :return: None
        """
        if to_zero:
            self.__no_sack_and_pawn_count = 0
            return
        self.__no_sack_and_pawn_count += 1

    def set_castling_queen_side(self, can_castle: bool, color: int) -> None:
        """
        Sets castling capabilities on queen side
        :param can_castle: bool value
        :param color: int value of color
        :return: None
        """
        if color == PiecesEnum.WHITE.value:
            self.__white_castle_queen = can_castle
        else:
            self.__black_castle_queen = can_castle

    def castle_king(self, piece: int, move: Move) -> None:
        """
        Method used to castle king it means prepare board for castling
        :param piece: int value of piece_square
        :param move: Move instance
        :return: None
        """
        distance = move.get_start_square() - move.get_end_square()

        if distance == MoveEnum.CASTLE_MOVE.value:
            color = ColorManager.get_piece_color(piece)
            rook_position = MoveValidator.get_rook_position(color, True)

            self.__board_array[move.get_start_square()] = 0
            self.__board_array[move.get_end_square()] = piece
            self.__board_array[rook_position] = 0
            self.__board_array[move.get_end_square() + 1] = color | PiecesEnum.ROOK.value
            self.set_castling_king_side(False, color)
            self.set_castling_queen_side(False, color)
        elif distance == -MoveEnum.CASTLE_MOVE.value:
            color = ColorManager.get_piece_color(piece)
            rook_position = MoveValidator.get_rook_position(color, False)

            self.__board_array[move.get_start_square()] = 0
            self.__board_array[move.get_end_square()] = piece
            self.__board_array[rook_position] = 0
            self.__board_array[move.get_end_square() - 1] = color | PiecesEnum.ROOK.value
            self.set_castling_king_side(False, color)
            self.set_castling_queen_side(False, color)
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

    def set_legal_moves(self, legal_moves: list[Move]) -> None:
        """
        Method used to set legal moves list
        :param legal_moves: list of legal moves
        :return: None
        """
        self.__legal_moves = legal_moves

    def set_opposite_move_color(self) -> None:
        """
        Method used to change the color of players pieces which is turn.
        :return: None
        """
        if self.__color_to_move == PiecesEnum.BLACK.value:
            self.__color_to_move = PiecesEnum.WHITE.value
        else:
            self.__color_to_move = PiecesEnum.BLACK.value

    def get_legal_moves(self) -> list[Move]:
        """
        Gives access to legal moves list.
        :return: list of moves
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

    def __init_starting_board(self) -> ndarray[int]:
        """
        Method initializes starting board.
        :return: board int array
        """
        board = zeros(BoardEnum.BOARD_SIZE.value)
        index = 0
        white_pieces = BoardInitializer.init_white_pieces_array()
        black_pieces = BoardInitializer.init_black_pieces_array()

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = black_pieces[index]
            index += 1

        index += 4 * BoardEnum.BOARD_LENGTH.value
        border_edge_index = 2 * BoardEnum.BOARD_LENGTH.value - 1

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = white_pieces[border_edge_index]
            border_edge_index -= 1
            index += 1
        return board

    def delete_piece_from_board(self, row: int, col: int) -> int:
        """
        Deletes piece_square from board and updates fen string.
        :param row: row int index
        :param col: col int index
        :return: deleted piece_square value
        """
        board_index = BoardEnum.BOARD_LENGTH.value * row + col

        piece = self.__board_array[board_index]
        self.__board_array[board_index] = 0
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
        board_index = BoardEnum.BOARD_LENGTH.value * row + col
        color = ColorManager.get_piece_color(self.__board_array[board_index])

        return color == self.__color_to_move

    def is_it_legal_move(self, move: Move) -> bool:
        """
        Checks if move given can be played
        :param move: current move player wants to play
        :return: bool value whether move is legal or not
        """
        return move in self.__legal_moves

    def update_fen(self):
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
        self.__board_array[self.__en_passant_square] = piece
        self.__board_array[self.__en_passant_piece_square] = 0

        self.__en_passant_square = MoveEnum.NONE_EN_PASSANT_SQUARE.value
        self.__en_passant_piece_square = MoveEnum.NONE_EN_PASSANT_SQUARE.value
        self.__fen_string = FenFactory.convert_board_array_to_fen(self)

    def set_en_passant_square(self, square: int) -> None:
        """
        Method used to set en passant square
        :param square: int value of square
        :return: None
        """
        self.__en_passant_square = square

    def set_en_passant_piece_square(self, piece_square: int) -> None:
        """
        Method used to set an en passant pieces quare value
        :param piece_square: int piece square value
        :return: None
        """
        self.__en_passant_piece_square = piece_square

    def get_en_passant_square(self) -> int:
        """
        Gives access to an en passant square value
        :return:
        """
        return self.__en_passant_square

    def get_en_passant_piece_square(self) -> int:
        """
        Gives access to an en passant piece square value
        :return:
        """
        return self.__en_passant_piece_square

    def make_move(self, move: Move, color: int) -> int:
        deleted_piece: int = self.__board_array[move.get_end_square()]

        self.__board_array[move.get_start_square()] = 0
        self.__board_array[move.get_end_square()] = color + move.get_moving_piece()

        return deleted_piece

    def un_make_move(self, move: Move, deleted_piece: int) -> None:
        moved_piece = self.__board_array[move.get_end_square()]
        self.__board_array[move.get_end_square()] = deleted_piece
        self.__board_array[move.get_start_square()] = moved_piece
