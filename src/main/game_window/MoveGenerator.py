from numpy import int8
from numpy import ndarray
from numpy import zeros

from game_window.CheckUtil import CheckUtil
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
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
        pseudo_legal_moves = MoveGenerator.generate_moves(color_to_move, board)
        legal_moves = []

        for move_to_verify in pseudo_legal_moves:
            is_it_valid_move = True
            deleted_piece = board.make_move(move_to_verify, color_to_move)
            opponent_moves = MoveGenerator.generate_moves(ColorManager.get_opposite_piece_color(color_to_move), board)
            kings_square = CheckUtil.find_friendly_king_squares(board.get_board_array(), color_to_move)

            for move in opponent_moves:
                if move_to_verify.get_special_flag_value() == SpecialFlags.CASTLING.value:
                    if move.get_end_square() in CheckUtil.get_castling_squares(move_to_verify):
                        is_it_valid_move = False
                        break
                if move.get_end_square() == kings_square:
                    is_it_valid_move = False
                    break
            if is_it_valid_move:
                legal_moves.append(move_to_verify)
            board.un_make_move(move_to_verify, deleted_piece)

        return legal_moves

    @staticmethod
    def generate_moves(color_to_move: int, board) -> list[Move]:
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
            elif piece == PiecesEnum.KNIGHT.value or piece == PiecesEnum.KING.value:
                MoveGenerator.generate_moves_for_knight_and_king(moves, piece, color_to_move, board, square)
            elif piece == PiecesEnum.PAWN.value:
                MoveGenerator.generate_pawn_moves(moves, piece, color_to_move, board, square)
        return moves

    @staticmethod
    def generate_sliding_piece_move(piece: int, start_square: int, moves: list[Move], color: int, board) -> None:
        """
        Static method used to generate moves for sliding pieces
        :param piece: int value of piece_square
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

    def generate_moves_for_knight_and_king(moves: list[Move], piece: int, color: int, board: 'Board', start_square: int) -> None:
        """
        Static method used to generate moves for knights and kings
        :param moves: list of moves
        :param piece: int value of piece_square
        :param color: int value of color to move
        :param board: board instance
        :param start_square: int index of current square
        :return: None
        """
        if piece == PiecesEnum.KING.value:
            directions = MoveEnum.KING_DIRECTIONS.value
            piece_range = MoveEnum.KING_RANGE.value
        else:
            directions = MoveEnum.KNIGHT_DIRECTIONS.value
            piece_range = MoveEnum.MAX_KNIGHT_JUMP.value

        for direction in range(MoveEnum.KK_DIRECTIONS_NUMBER.value):
            move_target = start_square + directions[direction]

            if move_target > BoardEnum.BOARD_SIZE.value - 1 or move_target < 0:
                continue
            if not MoveValidator.is_attack_target_in_border_bounds(start_square, move_target, piece_range):
                continue
            piece_on_move_target = board.get_board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            moves.append(Move(start_square, move_target, piece))

            if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                continue
        if piece == PiecesEnum.KING.value:
            MoveGenerator.generate_castling_moves(moves, piece, color, board, start_square)

    @staticmethod
    def generate_castling_moves(moves: list[Move], piece: int, color: int, board, start_square: int) -> None:
        """
        Static method to generate castling moves
        :param moves: list of moves
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start square index
        :return: None
        """
        if not MoveValidator.is_anything_on_king_side(board, start_square, color) and board.get_fen_data().can_king_castle_king_side(color):
            move_target = start_square + MoveEnum.CASTLE_MOVE.value
            moves.append(Move(start_square, move_target, piece, SpecialFlags.CASTLING.value))
        if not MoveValidator.is_anything_on_queen_side(board, start_square) and board.get_fen_data().can_king_castle_queen_side(color):
            move_target = start_square - MoveEnum.CASTLE_MOVE.value
            moves.append(Move(start_square, move_target, piece, SpecialFlags.CASTLING.value))

    @staticmethod
    def generate_pawn_moves(moves: list[Move], piece: int, color: int, board, start_square: int) -> None:
        """
        Static method to generate moves for pawns
        :param moves: list of moves
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start square index
        :return: None
        """
        MoveValidator.add_pawn_moves(start_square, piece, color, moves, board)
        MoveValidator.add_pawn_attacks(start_square, piece, color, moves, board)
