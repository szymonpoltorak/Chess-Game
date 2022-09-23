from numpy import int8
from numpy import ndarray
from numpy import zeros

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move
from game_window.MoveValidator import MoveValidator


class MoveGenerator:
    @staticmethod
    def calculate_distance_to_borders() -> ndarray[int]:
        """
        Calculates array of distances of each square in every direction to board borders.
        :return: ndarray of distances
        """
        distances = zeros((BoardEnum.BOARD_SIZE.value, BoardEnum.BOARD_LENGTH.value), dtype=int8)

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
                MoveGenerator.generate_sliding_piece_move(piece, square, moves, color_to_move, board)
            if piece == PiecesEnum.KNIGHT.value:
                MoveGenerator.generate_moves_for_knight(moves, piece, color_to_move, board, square)
            if piece == PiecesEnum.KING.value:
                MoveGenerator.generate_moves_for_king(moves, piece, color_to_move, board, square)
            if piece == PiecesEnum.PAWN.value:
                MoveGenerator.generate_pawn_moves(moves, piece, color_to_move, board, square)
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

            if not MoveValidator.is_knight_move_target_in_borders(start_square, move_target):
                continue
            piece_on_move_target = board.get_board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            moves.append(Move(start_square, move_target, piece))

            if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                continue

    @staticmethod
    def generate_moves_for_king(moves: list[Move], piece: int, color: int, board, start_square: int) -> None:
        """
        Static method use to generate possible moves for king.
        :param moves: list of moves
        :param piece: int value of a piece
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start square index
        :return: None
        """
        for direction in range(MoveEnum.KING_DIRECTIONS_NUMBER.value):
            move_target = start_square + MoveEnum.KING_DIRECTIONS.value[direction]

            if not MoveValidator.is_king_move_target_in_borders(start_square, move_target):
                continue
            piece_on_move_target = board.get_board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            moves.append(Move(start_square, move_target, piece))

            if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                continue
        MoveGenerator.generate_castling_moves(moves, piece, color, board, start_square)

    @staticmethod
    def generate_castling_moves(moves: list[Move], piece: int, color: int, board, start_square: int) -> None:
        """
        Static method to generate castling moves
        :param moves: list of moves
        :param piece: int value of a piece
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start square index
        :return: None
        """
        if not MoveValidator.is_anything_on_king_side(board, start_square, color) and board.can_king_castle_king_side(color):
            move_target = start_square + MoveEnum.CASTLE_MOVE.value
            moves.append(Move(start_square, move_target, piece))
        if not MoveValidator.is_anything_on_queen_side(board, start_square) and board.can_king_castle_queen_side(color):
            move_target = start_square - MoveEnum.CASTLE_MOVE.value
            moves.append(Move(start_square, move_target, piece))

    @staticmethod
    def generate_pawn_moves(moves: list[Move], piece: int, color: int, board, start_square: int) -> None:
        """
        Static method to generate moves for pawns
        :param moves: list of moves
        :param piece: int value of a piece
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start square index
        :return: None
        """
        MoveValidator.add_pawn_moves(start_square, piece, color, moves, board)
        MoveValidator.add_pawn_attacks(start_square, piece, color, moves, board)
