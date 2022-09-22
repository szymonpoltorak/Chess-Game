from numpy import int32
from numpy import ndarray
from numpy import zeros

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move


class MoveValidator:
    @staticmethod
    def calculate_distance_to_borders() -> ndarray[int]:
        """
        Calculates array of distances of each square in every direction to board borders.
        :return: ndarray of distances
        """
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

    @staticmethod
    def generate_legal_moves(color_to_move: int, board) -> list[Move]:
        """
        Static method used  to generate legal moves for pieces of given color
        :param color_to_move: int value of color to be moved
        :param board: Board instance == representation of board
        :return: list of all legal moves
        """
        moves = []

        for square in range(BoardEnum.BOARD_SIZE.value):
            piece_color = ColorManager.get_piece_color(board.get_board_array()[square])
            piece = board.get_board_array()[square] - piece_color

            if color_to_move != piece_color:
                continue

            if MoveValidator.is_sliding_piece(piece):
                MoveValidator.generate_sliding_piece_move(piece, square, moves, color_to_move, board)

            if piece == PiecesEnum.KNIGHT.value:
                MoveValidator.generate_moves_for_knight(moves, piece, color_to_move, board, square)
        return moves

    @staticmethod
    def generate_sliding_piece_move(piece: int, start_square: int, moves: list[Move], color: int, board) -> None:
        """
        Static method used to generate moves for sliding pieces
        :param piece: int value of piece
        :param start_square: int index of current square
        :param moves: list of moves
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        for direction in range(MoveEnum.SLIDING_DIRECTIONS_NUMBER.value):
            for direction_step in range(board.get_distances()[start_square][direction]):
                if not MoveValidator.is_it_sliding_piece(piece, MoveEnum.SLIDING_DIRECTIONS.value[direction]):
                    continue
                move_target = start_square + MoveEnum.SLIDING_DIRECTIONS.value[direction] * (direction_step + 1)
                piece_on_move_target = board.get_board_array()[move_target]

                if ColorManager.get_piece_color(piece_on_move_target) == color:
                    break
                moves.append(Move(start_square, move_target, piece))

                if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                    break

    @staticmethod
    def is_it_sliding_piece(piece: int, direction: int) -> bool:
        """
        Static method used to check if this move should be calculated
        :param piece: int value of piece
        :param direction: int value of direction
        :return: bool value of if move should be calculated or not
        """
        diagonal_pieces = (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value)
        diagonal_directions = (MoveEnum.TOP_LEFT_S.value, MoveEnum.TOP_RIGHT_S.value, MoveEnum.BOTTOM_LEFT_S.value,
                               MoveEnum.BOTTOM_RIGHT_S.value)

        line_pieces = (PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)
        line_directions = (MoveEnum.TOP_S.value, MoveEnum.LEFT_S.value, MoveEnum.RIGHT_S.value, MoveEnum.BOTTOM_S.value)

        if piece in diagonal_pieces and direction in diagonal_directions:
            return True
        return piece in line_pieces and direction in line_directions

    @staticmethod
    def is_sliding_piece(piece: int) -> bool:
        """
        Static method used to check if piece is a sliding piece.
        :param piece: int value of piece
        :return: bool value of if piece is sliding piece or not
        """
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)

    @staticmethod
    def generate_moves_for_knight(moves: list[Move], piece: int, color: int, board, start_square: int) -> None:
        """
        Static method used to generate moves for knights
        :param moves: list of moves
        :param piece: int value of piece
        :param color: int value of color to move
        :param board: board instance
        :param start_square: int index of current square
        :return: None
        """
        for direction in range(MoveEnum.KNIGHT_DIRECTIONS_NUMBER.value):
            move_target = start_square + MoveEnum.KNIGHT_DIRECTIONS.value[direction]

            if not MoveValidator.is_move_target_in_borders(start_square, move_target):
                continue
            piece_on_move_target = board.get_board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            moves.append(Move(start_square, move_target, piece))

            if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                continue

    @staticmethod
    def is_move_target_in_borders(start_square: int, move_target: int) -> bool:
        """
        Checks if piece move target is in bounds of chess board
        :param start_square: int index of start square
        :param move_target: int index of move target square
        :return: bool
        """
        start_col = start_square % BoardEnum.BOARD_LENGTH.value
        target_col = move_target % BoardEnum.BOARD_LENGTH.value

        if move_target > BoardEnum.BOARD_SIZE.value - 1 or move_target < 0:
            return False
        return abs(start_col - target_col) <= MoveEnum.MAX_KNIGHT_JUMP.value
