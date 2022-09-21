from numpy import array
from numpy import int32
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
    __slots__ = array(["__board_array", "__fen_string", "__color_to_move", "__legal_moves", "__distances_to_borders"])

    def __init__(self):
        self.__board_array: ndarray[int] = self.__init_starting_board()
        self.__fen_string: str = BoardEnum.STARTING_POSITION.value
        self.__color_to_move: int = PiecesEnum.WHITE.value
        self.__distances_to_borders: ndarray[int] = self.calculate_distance_to_borders()
        self.__legal_moves: list[Move] = self.generate_legal_moves(PiecesEnum.WHITE.value)

    def generate_legal_moves(self, color_to_move: int) -> list[Move]:
        moves = []

        for square in range(BoardEnum.BOARD_SIZE.value):
            piece_color = self.get_piece_color(self.__board_array[square])
            piece = self.__board_array[square] - piece_color

            if color_to_move != piece_color:
                continue

            if self.is_sliding_piece(piece):
                moves = self.generate_sliding_piece_move(piece, square, moves, color_to_move)

        return moves

    def is_sliding_piece(self, piece: int) -> bool:
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)

    def generate_sliding_piece_move(self, piece: int, start_square: int, moves: list[Move], color: int) -> list[Move]:
        for direction in range(MoveEnum.SLIDING_DIRECTIONS.value):
            for direction_step in range(self.__distances_to_borders[start_square][direction]):
                if not self.should_this_move_be_calculated(piece, MoveEnum.DIRECTIONS.value[direction]):
                    continue
                move_target = start_square + MoveEnum.DIRECTIONS.value[direction] * (direction_step + 1)
                piece_on_move_target = self.__board_array[move_target]

                if self.get_piece_color(piece_on_move_target) == color:
                    break
                moves.append(Move(start_square, move_target, piece))

                if self.get_piece_color(piece_on_move_target) == self.get_opposite_piece_color(color):
                    break
        return moves

    def should_this_move_be_calculated(self, piece: int, direction: int) -> bool:
        diagonal_pieces = (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value)
        diagonal_directions = (MoveEnum.TOP_LEFT.value, MoveEnum.TOP_RIGHT.value, MoveEnum.BOTTOM_LEFT.value,
                               MoveEnum.BOTTOM_RIGHT.value)

        line_pieces = (PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)
        line_directions = (MoveEnum.TOP.value, MoveEnum.LEFT.value, MoveEnum.RIGHT.value, MoveEnum.BOTTOM.value)

        if piece in diagonal_pieces and direction in diagonal_directions:
            return True
        return piece in line_pieces and direction in line_directions

    def set_legal_moves(self, legal_moves: list[Move]) -> None:
        self.__legal_moves = legal_moves

    def calculate_distance_to_borders(self) -> ndarray[int]:
        distances = zeros((BoardEnum.BOARD_SIZE.value, BoardEnum.BOARD_LENGTH.value), dtype=int32)

        for row in range(BoardEnum.BOARD_LENGTH.value):
            for col in range(BoardEnum.BOARD_LENGTH.value):
                squares_to_top = row
                squares_to_bottom = 7 - row
                square_to_left = col
                squares_to_right = 7 - col
                squares_to_top_left = min(squares_to_top, square_to_left)
                squares_to_top_right = min(squares_to_top, squares_to_right)
                squares_to_bottom_right = min(squares_to_bottom, squares_to_right)
                squares_to_bottom_left = min(squares_to_bottom, square_to_left)
                square_index = 8 * row + col

                distances[square_index] = [
                    squares_to_top_left,
                    squares_to_top,
                    squares_to_top_right,
                    square_to_left,
                    squares_to_right,
                    squares_to_bottom_left,
                    squares_to_bottom,
                    squares_to_bottom_right
                ]
        return distances

    def get_legal_moves(self) -> list[Move]:
        return self.__legal_moves

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
        board_index = BoardEnum.BOARD_LENGTH.value * row + col
        color = self.get_piece_color(self.__board_array[board_index])

        return color == self.__color_to_move

    def set_opposite_move_color(self) -> None:
        if self.__color_to_move == PiecesEnum.BLACK.value:
            self.__color_to_move = PiecesEnum.WHITE.value
        else:
            self.__color_to_move = PiecesEnum.BLACK.value

    def get_opposite_piece_color(self, color: int) -> int:
        if color == PiecesEnum.BLACK.value:
            return PiecesEnum.WHITE.value
        return PiecesEnum.BLACK.value

    def is_it_legal_move(self, move: Move) -> bool:
        if move.get_moving_piece() in (PiecesEnum.BISHOP.value, PiecesEnum.ROOK.value, PiecesEnum.QUEEN.value):
            return move in self.__legal_moves
        return True
