import numpy
from numpy import array
from numpy import ndarray
from numpy import zeros

from game_window.BoardInitializer import BoardInitializer
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.FenFactory import FenFactory
from game_window.Move import Move


class Board:
    """
    Class to hold and manage board representation.
    """
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__valid_moves", "__distances_to_borders"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders: ndarray[int] = self.calculate_distance_to_borders()
        #print(self.__distances_to_borders)
        self.__valid_moves: list[Move] = self.generate_legal_moves(PiecesEnum.WHITE.value)
        print(self.__board_array)
        print(self.__valid_moves)

    def generate_legal_moves(self, color_to_move: int) -> list[Move]:
        moves = []

        for starting_square in range(BoardEnum.BOARD_SIZE.value):
            piece = self.__board_array[starting_square] - color_to_move

            if color_to_move != self.get_piece_color(piece):
                continue

            if self.is_sliding_piece(piece):
                self.generate_sliding_piece_move(piece, starting_square, moves, color_to_move)

        return moves

    def is_sliding_piece(self, piece: int) -> bool:
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)

    def generate_sliding_piece_move(self, piece: int, start_square: int, moves: list[Move], color: int):
        start_index = self.calculate_start_index(piece)
        end_index = self.calculate_end_index(piece)

        for direction_index in range(start_index, end_index):
            for square in range(self.__distances_to_borders[start_square][direction_index]):
                move_target = start_square + MoveEnum.DIRECTIONS.value[direction_index] * (square + 1)
                piece_on_moves_target = self.__board_array[move_target]

                if self.get_piece_color(piece_on_moves_target) == color:
                    break
                moves.append(Move(start_square, move_target, piece))

                if self.get_piece_color(piece_on_moves_target) == self.get_opposite_piece_color(color):
                    break

    def calculate_distance_to_borders(self) -> ndarray[int]:
        distances = zeros((BoardEnum.BOARD_SIZE.value, BoardEnum.BOARD_LENGTH.value), dtype=numpy.int32)

        for row in range(BoardEnum.BOARD_LENGTH.value):
            for col in range(BoardEnum.BOARD_LENGTH.value):
                squares_to_top = 7 - row
                squares_to_bottom = row
                square_to_left = col
                squares_to_right = 7 - col
                square_index = 8 * row + col
                #print(f"Row: {row} Col: {col}")
                #print(f"Top {squares_to_top} Bottom {squares_to_bottom} Left {square_to_left} Right {squares_to_right}")
                print(f"Square Index: {square_index}")

                distances[square_index] = [
                    squares_to_top,
                    squares_to_bottom,
                    square_to_left,
                    squares_to_right,
                    min(squares_to_top, square_to_left),
                    min(squares_to_bottom, squares_to_right),
                    min(squares_to_top, squares_to_right),
                    min(squares_to_bottom, square_to_left)
                ]
                print(distances[square_index])

        return distances

    def calculate_start_index(self, piece: int) -> int:
        if piece == PiecesEnum.BISHOP.value:
            return MoveEnum.BISHOP_START_INDEX.value
        return MoveEnum.PIECE_START_INDEX.value

    def calculate_end_index(self, piece: int) -> int:
        if piece == PiecesEnum.ROOK.value:
            return MoveEnum.ROOK_END_INDEX.value
        return MoveEnum.PIECE_END_INDEX.value

    def get_legal_moves(self):
        return self.__valid_moves

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

        index += 32
        j = 15

        for _ in range(2 * BoardEnum.BOARD_LENGTH.value):
            board[index] = white_pieces[j]
            j -= 1
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

    def get_piece_color(self, piece: int) -> int:
        if piece == PiecesEnum.NONE.value:
            return PiecesEnum.NONE.value
        elif piece - PiecesEnum.BLACK.value < 0:
            return PiecesEnum.WHITE.value
        return PiecesEnum.BLACK.value

    def add_piece_to_the_board(self, piece: int, row: int, col: int) -> None:
        """
        Adds piece to board array and updates fen string.
        :param piece: int value of piece
        :param row: int row index
        :param col: int col index
        :return: None
        """
        board_index = BoardEnum.BOARD_LENGTH.value * row + col

        self.__board_array[board_index] = piece
        self.__fen_string = FenFactory.convert_board_array_to_fen(self.__board_array)

    def should_this_piece_move(self, row: int, col: int) -> bool:
        board_index = BoardEnum.BOARD_LENGTH.value * row + col
        color = self.get_piece_color(self.__board_array[board_index])

        if color != self.__color_to_move:
            return False
        return True

    def set_opposite_move_color(self) -> None:
        if self.__color_to_move == PiecesEnum.BLACK.value:
            self.__color_to_move = PiecesEnum.WHITE.value
        else:
            self.__color_to_move = PiecesEnum.BLACK.value

    def get_opposite_piece_color(self, color: int) -> int:
        if color == PiecesEnum.BLACK.value:
            return PiecesEnum.WHITE.value
        return PiecesEnum.BLACK.value

    def is_it_legal_move(self, move: Move):
        if move.get_moving_piece() in (PiecesEnum.BISHOP.value, PiecesEnum.ROOK.value, PiecesEnum.QUEEN.value):
            print("\nI was here")
            print(move in self.__valid_moves)
            return move in self.__valid_moves
        return True
