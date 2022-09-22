from numpy import array
from numpy import ndarray
from numpy import zeros

from game_window.BoardInitializer import BoardInitializer
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.FenFactory import FenFactory
from game_window.Move import Move
from game_window.MoveValidator import MoveValidator


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders",
                       "__white_castle_king", "__white_castle_queen",  "__black_castle_king", "__black_castle_queen"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__white_castle_king = True
        self.__white_castle_queen = True
        self.__black_castle_king = True
        self.__black_castle_queen = True
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders = MoveValidator.calculate_distance_to_borders()
        self.__legal_moves = MoveValidator.generate_legal_moves(self.__color_to_move, self)

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
        :param piece: int value of piece
        :param move: Move instance
        :return: None
        """
        distance = move.get_start_square() - move.get_end_square()

        if distance == 2:
            color = ColorManager.get_piece_color(piece)
            rook_position = MoveValidator.get_rook_position(color, True)

            self.__board_array[move.get_start_square()] = 0
            self.__board_array[move.get_end_square()] = piece
            self.__board_array[rook_position] = 0
            self.__board_array[move.get_end_square() + 1] = color | PiecesEnum.ROOK.value
            self.set_castling_king_side(False, color)
            self.set_castling_queen_side(False, color)
        elif distance == -2:
            color = ColorManager.get_piece_color(piece)
            rook_position = MoveValidator.get_rook_position(color, False)
            print(f"\nColor : {color}\nRook Position : {rook_position}")

            self.__board_array[move.get_start_square()] = 0
            self.__board_array[move.get_end_square()] = piece
            self.__board_array[rook_position] = 0
            self.__board_array[move.get_end_square() - 1] = color | PiecesEnum.ROOK.value
            self.set_castling_king_side(False, color)
            self.set_castling_queen_side(False, color)
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)

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
        Deletes piece from board and updates fen string.
        :param row: row int index
        :param col: col int index
        :return: deleted piece value
        """
        board_index = BoardEnum.BOARD_LENGTH.value * row + col

        piece = self.__board_array[board_index]
        self.__board_array[board_index] = 0
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)

        return piece

    def add_piece_to_the_board(self, piece: int, square: int) -> None:
        """
        Adds piece to board array and updates fen string.
        :param piece: int value of piece
        :param square: int index of where to add a piece
        :return: None
        """
        self.__board_array[square] = piece
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)

    def should_this_piece_move(self, row: int, col: int) -> bool:
        """
        Checks if piece on boards row and col indexes should move.
        :param row: int value of row index
        :param col: int value of col index
        :return: bool value if piece should move or not
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
        if move.get_moving_piece() in (PiecesEnum.BISHOP.value, PiecesEnum.ROOK.value, PiecesEnum.QUEEN.value,
                                       PiecesEnum.KNIGHT.value, PiecesEnum.KING.value):
            return move in self.__legal_moves
        return True
