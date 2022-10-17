from typing import TYPE_CHECKING

from numpy import full
from numpy import int8
from numpy import ndarray
from numpy import zeros

from game_window.CheckUtil import CheckUtil
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.FenData import FenData
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveList import MoveList
from game_window.moving.MoveUtil import MoveUtil
from game_window.moving.MoveValidator import MoveValidator

if TYPE_CHECKING:
    from game_window.Board import Board


class MoveGenerator:
    __slots__ = ()

    @staticmethod
    def calculate_distance_to_borders() -> ndarray[int]:
        """
        Calculates array of distances of each end_square in every direction to board borders.
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
    def generate_legal_moves(color_to_move: int, board: 'Board') -> MoveList:
        # TODO when rook is being captured for example by knight it does not disappear and does not disable castling
        pseudo_legal_moves: MoveList = MoveGenerator.generate_moves(color_to_move, board)
        legal_moves: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

        for move_to_verify in pseudo_legal_moves.moves:
            if move_to_verify is None:
                break
            is_it_valid_move: bool = True
            deleted_data: MoveData = MoveUtil.make_move(move_to_verify, color_to_move, board)
            opponent_moves: MoveList = MoveGenerator.generate_moves(ColorManager.get_opposite_piece_color(color_to_move), board)
            kings_square: int = CheckUtil.find_friendly_king_squares(board.get_board_array(), color_to_move)

            for move in opponent_moves.moves:
                if move is None:
                    break
                if move_to_verify.get_special_flag_value() == SpecialFlags.CASTLING.value:
                    if move.get_end_square() in CheckUtil.get_castling_squares(move_to_verify):
                        is_it_valid_move: bool = False
                        break
                if move.get_end_square() == kings_square:
                    is_it_valid_move: bool = False
                    break
            if is_it_valid_move:
                legal_moves.moves[legal_moves.free_index] = move_to_verify
                legal_moves.free_index += 1
            MoveUtil.un_make_move(move_to_verify, deleted_data, board)

        return legal_moves

    @staticmethod
    def generate_moves(color_to_move: int, board: 'Board') -> MoveList:
        """
        Static method used  to generate legal moves_list for pieces of given color
        :param color_to_move: int value of color to be moved
        :param board: Board instance == representation of board
        :return: list of all legal moves
        """
        moves_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)

        for square in range(BoardEnum.BOARD_SIZE.value):
            piece_color: int = ColorManager.get_piece_color(board.get_board_array()[square])
            piece: int = board.get_board_array()[square] - piece_color

            if color_to_move != piece_color:
                continue

            if MoveValidator.is_sliding_piece(piece):
                MoveGenerator.generate_sliding_piece_move(piece, square, moves_list, color_to_move, board)
            elif piece == PiecesEnum.KNIGHT.value or piece == PiecesEnum.KING.value:
                MoveGenerator.generate_moves_for_knight_and_king(moves_list, piece, color_to_move, board, square)
            elif piece == PiecesEnum.PAWN.value:
                MoveGenerator.generate_pawn_moves(moves_list, piece, color_to_move, board, square)
        return moves_list

    @staticmethod
    def generate_sliding_piece_move(piece: int, start_square: int, moves_list: MoveList, color: int, board: 'Board') -> None:
        """
        Static method used to generate moves_list for sliding pieces
        :param piece: int value of piece_square
        :param start_square: int index of current end_square
        :param moves_list: list of moves_list
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        for direction in range(MoveEnum.SLIDING_DIRECTIONS_NUMBER.value):
            for direction_step in range(board.get_distances()[start_square][direction]):
                if not MoveValidator.is_it_sliding_piece(piece, MoveEnum.SLIDING_DIRECTIONS.value[direction]):
                    continue
                move_target: int = start_square + MoveEnum.SLIDING_DIRECTIONS.value[direction] * (direction_step + 1)
                piece_on_move_target: int = board.get_board_array()[move_target]

                if ColorManager.get_piece_color(piece_on_move_target) == color:
                    break
                moves_list.moves[moves_list.free_index] = Move(start_square, move_target, piece, SpecialFlags.NONE.value)
                moves_list.free_index += 1

                if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                    break

    @staticmethod
    def generate_moves_for_knight_and_king(moves_list: MoveList, piece: int, color: int, board: 'Board', start_square: int) -> None:
        """
        Static method used to generate moves_list for knights and kings
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of piece_square
        :param color: int value of color to move
        :param board: board instance
        :param start_square: int index of current end_square
        :return: None
        """
        if piece == PiecesEnum.KING.value:
            directions: tuple[int] = MoveEnum.KING_DIRECTIONS.value
            piece_range: int = MoveEnum.KING_RANGE.value
        else:
            directions: tuple[int] = MoveEnum.KNIGHT_DIRECTIONS.value
            piece_range: int = MoveEnum.MAX_KNIGHT_JUMP.value

        for direction in range(MoveEnum.KK_DIRECTIONS_NUMBER.value):
            move_target: int = start_square + directions[direction]

            if move_target > BoardEnum.BOARD_SIZE.value - 1 or move_target < 0:
                continue
            if not MoveValidator.is_attack_target_in_border_bounds(start_square, move_target, piece_range):
                continue
            piece_on_move_target: int = board.get_board_array()[move_target]

            if ColorManager.get_piece_color(piece_on_move_target) == color:
                continue
            moves_list.moves[moves_list.free_index] = Move(start_square, move_target, piece, SpecialFlags.NONE.value)
            moves_list.free_index += 1

            if ColorManager.get_piece_color(piece_on_move_target) == ColorManager.get_opposite_piece_color(color):
                continue
        if piece == PiecesEnum.KING.value:
            MoveGenerator.generate_castling_moves(moves_list, piece, color, board, start_square)

    @staticmethod
    def generate_castling_moves(moves_list: MoveList, piece: int, color: int, board: 'Board', start_square: int) -> None:
        """
        Static method to generate castling moves_list
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start end_square index
        :return: None
        """
        fen_data: FenData = board.get_fen_data()

        if not MoveValidator.is_anything_on_king_side(board, start_square) and fen_data.can_king_castle_king_side(color):
            if not MoveValidator.is_board_inverted(board):
                move_target: int = start_square + MoveEnum.CASTLE_MOVE.value
            else:
                move_target: int = start_square - MoveEnum.CASTLE_MOVE.value
            moves_list.moves[moves_list.free_index] = Move(start_square, move_target, piece, SpecialFlags.CASTLING.value)
            moves_list.free_index += 1
            
        if not MoveValidator.is_anything_on_queen_side(board, start_square) and fen_data.can_king_castle_queen_side(color):
            if not MoveValidator.is_board_inverted(board):
                move_target: int = start_square - MoveEnum.CASTLE_MOVE.value
            else:
                move_target: int = start_square + MoveEnum.CASTLE_MOVE.value
            moves_list.moves[moves_list.free_index] = Move(start_square, move_target, piece,
                                                           SpecialFlags.CASTLING.value)
            moves_list.free_index += 1

    @staticmethod
    def generate_pawn_moves(moves_list: MoveList, piece: int, color: int, board: 'Board', start_square: int) -> None:
        """
        Static method to generate moves_list for pawns
        :param moves_list: list of moves_list (MoveList instance)
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param board: Board instance
        :param start_square: start end_square index
        :return: None
        """
        MoveValidator.add_pawn_moves(start_square, piece, color, moves_list, board)
        MoveValidator.add_pawn_attacks(start_square, piece, color, moves_list, board)
