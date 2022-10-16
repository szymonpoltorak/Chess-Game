from typing import TYPE_CHECKING

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.FenData import FenData
from game_window.moving.Move import Move
from game_window.moving.MoveList import MoveList

if TYPE_CHECKING:
    from game_window.Board import Board


class MoveValidator:
    __slots__ = ()

    @staticmethod
    def is_anything_on_king_side(board: 'Board', start_square: int) -> bool:
        """
        Checks if there is anything on the path between a king side rook and the king
        :param board: Board instance
        :param start_square: int index of kings end_square
        :return: bool
        """
        step = -1 if MoveValidator.is_board_inverted(board) else 1

        return MoveValidator.check_castling_squares(step, MoveEnum.KING_SIDE.value, start_square, board)

    @staticmethod
    def is_anything_on_queen_side(board: 'Board', start_square: int) -> bool:
        """
        Checks if there is anything on the path between a queen side rook and the king
        :param board: Board instance
        :param start_square: int index of kings end_square
        :return: bool
        """
        step = -1 if MoveValidator.is_board_inverted(board) else 1

        return MoveValidator.check_castling_squares(step, MoveEnum.QUEEN_SIDE.value, start_square, board)

    @staticmethod
    def check_castling_squares(step: int, side_value: int, start_square: int, board: 'Board'):
        for i in range(1, side_value + 1):
            index: int = start_square + step * i

            if index > 63 or index < 0:
                break
            if board.get_board_array()[start_square + step * i] != 0:
                return True
        return False

    @staticmethod
    def is_it_castling(move: Move) -> bool:
        """
        Checks if this move is castling
        :param move: Move instance
        :return: bool
        """
        move_length: int = abs(move.get_end_square() - move.get_start_square())

        return move.get_moving_piece() == PiecesEnum.KING.value and move_length == MoveEnum.CASTLE_MOVE.value

    @staticmethod
    def is_board_inverted(board: 'Board'):
        return board.get_engine_color() == PiecesEnum.WHITE.value

    @staticmethod
    def get_rook_position(color: int, is_queen_side: bool, upper_color: int, down_color: int) -> int:
        """
        Static method to return rooks board position based on given parameters
        :param down_color: value of down pieces color
        :param upper_color: value of upper pieces color
        :param color: rook color
        :param is_queen_side: bool
        :return: int value of rook position
        """
        move_dict = {
            (True, down_color): MoveEnum.BOTTOM_ROOK_QUEEN.value,
            (True, upper_color): MoveEnum.TOP_ROOK_QUEEN.value,
            (False, down_color): MoveEnum.BOTTOM_ROOK_KING.value,
            (False, upper_color): MoveEnum.TOP_ROOK_KING.value
        }
        return move_dict[is_queen_side, color]

    @staticmethod
    def disable_castling_on_side(color: int, move: Move, board: 'Board') -> None:
        """
        Disable castling for king on given side
        :param color: int value of color
        :param move: Move instance
        :param board: Board instance
        :return: None
        """
        engine_color: int = board.get_engine_color()
        player_color: int = board.get_player_color()
        start_square: int = move.get_start_square()
        fen_data: FenData = board.get_fen_data()

        if color == engine_color and start_square == MoveEnum.TOP_ROOK_QUEEN.value:
            fen_data.set_castling_queen_side(False, color)
        elif color == engine_color and start_square == MoveEnum.TOP_ROOK_KING.value:
            fen_data.set_castling_king_side(False, color)
        elif color == player_color and start_square == MoveEnum.BOTTOM_ROOK_QUEEN.value:
            fen_data.set_castling_queen_side(False, color)
        elif color == player_color and start_square == MoveEnum.BOTTOM_ROOK_KING.value:
            fen_data.set_castling_king_side(False, color)

    @staticmethod
    def is_attack_target_in_border_bounds(start_square: int, move_target: int, attack_range: int) -> bool:
        """
        Static method to check if pawns attack target is in board bonds
        :param start_square: int index of start end_square
        :param move_target: int index of attack target end_square
        :param attack_range: int value of range attack
        :return: bool
        """
        start_col: int = start_square % BoardEnum.BOARD_LENGTH.value
        target_col: int = move_target % BoardEnum.BOARD_LENGTH.value

        return abs(start_col - target_col) <= attack_range

    @staticmethod
    def is_it_sliding_piece(piece: int, direction: int) -> bool:
        """
        Static method used to check if this move should be calculated
        :param piece: int value of piece_square
        :param direction: int value of direction
        :return: bool value of if move should be calculated or not
        """
        diagonal_pieces: tuple[int, int] = (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value)
        diagonal_directions: tuple[int, int, int, int] = (MoveEnum.TOP_LEFT_S.value, MoveEnum.TOP_RIGHT_S.value,
                                                          MoveEnum.BOTTOM_LEFT_S.value, MoveEnum.BOTTOM_RIGHT_S.value)

        line_pieces: tuple[int, int] = (PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)
        line_directions: tuple[int, int, int, int] = (MoveEnum.TOP_S.value, MoveEnum.LEFT_S.value,
                                                      MoveEnum.RIGHT_S.value, MoveEnum.BOTTOM_S.value)

        if piece in diagonal_pieces and direction in diagonal_directions:
            return True
        return piece in line_pieces and direction in line_directions

    @staticmethod
    def is_sliding_piece(piece: int) -> bool:
        """
        Static method used to check if piece_square is a sliding piece_square.
        :param piece: int value of piece_square
        :return: bool value of if piece_square is sliding piece_square or not
        """
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)

    @staticmethod
    def add_pawn_moves(start_square: int, piece: int, color: int, moves_list: MoveList, board: 'Board') -> None:
        """
        Adds possible pawn movements
        :param start_square: int index of starting end_square
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param moves_list: list of moves_list (MoveList instance)
        :param board: Board instance
        :return: None
        """
        move_target: int = start_square
        double_move_target: int = start_square
        direction: int = 1
        pawn_index_bounds_min: int = 48
        pawn_index_bounds_max: int = 55
        upper_color: int = board.get_engine_color()
        down_color: int = ColorManager.get_opposite_piece_color(upper_color)

        if color == down_color:
            if double_move_target < 0 or move_target < 0:
                return
        else:
            if double_move_target > 63 or move_target > 63:
                return
            direction: int = -1
            pawn_index_bounds_min: int = 8
            pawn_index_bounds_max: int = 15

        move_target += direction * MoveEnum.PAWN_UP_SINGLE_MOVE.value
        double_move_target += direction * MoveEnum.PAWN_UP_SINGLE_MOVE.value * 2

        if pawn_index_bounds_min <= start_square <= pawn_index_bounds_max and MoveValidator.no_piece_in_pawns_way(
                                                    double_move_target, start_square, board,
                                                    direction * MoveEnum.PAWN_UP_SINGLE_MOVE.value):
            moves_list.moves[moves_list.free_index] = Move(start_square, double_move_target, piece, SpecialFlags.NONE.value)
            moves_list.free_index += 1
        if board.get_board_array()[move_target] == 0:
            MoveValidator.add_moves_and_promotions(start_square, move_target, piece, moves_list)

    @staticmethod
    def no_piece_in_pawns_way(double_move_target: int, start_square: int, board, step: int) -> bool:
        """
        Static method used to check if there is any piece_square on pawns way
        :param double_move_target: int target end_square of pawns double move
        :param start_square: int index of starting end_square
        :param board: Board instance
        :param step: int value of step
        :return: bool
        """
        piece_single_up: int = board.get_board_array()[start_square + step]
        piece_double_up: int = board.get_board_array()[double_move_target]

        return piece_double_up == 0 and piece_single_up == 0

    @staticmethod
    def add_pawn_attacks(start_square: int, piece: int, color: int, moves_list: MoveList, board: 'Board') -> None:
        """
        Static method used to add pawn attacks
        :param start_square: int index of starting end_square
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param moves_list: list of moves_list (MoveList instance)
        :param board: Board instance
        :return: None
        """
        left_piece_square: int = start_square + MoveValidator.get_attack_direction(color, "LEFT", board.get_engine_color())
        right_piece_square: int = start_square + MoveValidator.get_attack_direction(color, "RIGHT", board.get_engine_color())

        if left_piece_square < 0 or left_piece_square > 63 or right_piece_square < 0 or right_piece_square > 63:
            return
        left_piece: int = board.get_board_array()[left_piece_square]
        right_piece: int = board.get_board_array()[right_piece_square]

        if color != ColorManager.get_piece_color(left_piece) and left_piece != PiecesEnum.NONE.value:
            if MoveValidator.is_attack_target_in_border_bounds(start_square, left_piece_square,
                                                               MoveEnum.PAWN_RANGE.value):
                MoveValidator.add_moves_and_promotions(start_square, left_piece_square, piece, moves_list)
        if color != ColorManager.get_piece_color(right_piece) and right_piece != PiecesEnum.NONE.value:
            if MoveValidator.is_attack_target_in_border_bounds(start_square, right_piece_square,
                                                               MoveEnum.PAWN_RANGE.value):
                MoveValidator.add_moves_and_promotions(start_square, right_piece_square, piece, moves_list)
        MoveValidator.check_en_passant_movement(start_square, piece, color, moves_list, board)

    @staticmethod
    def add_moves_and_promotions(start_square: int, move_target: int, piece: int, moves_list: MoveList) -> None:
        """
        Checks if move is a promotion or not and add move to the list
        :param move_target: int target end_square of the move
        :param start_square: int index of starting end_square
        :param piece: int value of a piece_square
        :param moves_list: list of moves_list (MoveList instance)
        :return: None
        """
        if 56 <= move_target <= 63 or 0 <= move_target <= 7:
            for flag in range(SpecialFlags.PROMOTE_TO_QUEEN.value, SpecialFlags.PROMOTE_TO_BISHOP.value + 1):
                moves_list.moves[moves_list.free_index] = Move(start_square, move_target, piece, flag)
                moves_list.free_index += 1
        else:
            moves_list.moves[moves_list.free_index] = Move(start_square, move_target, piece, SpecialFlags.NONE.value)
            moves_list.free_index += 1

    @staticmethod
    def check_en_passant_movement(start_square: int, piece: int, color: int, moves_list: MoveList, board: 'Board') -> None:
        """
        Checks if there is an en passant movement and add it to list
        :param start_square:
        :param piece: int value of piece
        :param color: int value of color
        :param moves_list: list of moves (MoveList instance)
        :param board: Board instance
        :return: None
        """
        upper_color: int = board.get_engine_color()
        en_passant_square: int = board.get_fen_data().get_en_passant_square()
        en_passant_target_left: int = start_square + MoveValidator.get_attack_direction(color, "LEFT", upper_color)
        en_passant_target_right: int = start_square + MoveValidator.get_attack_direction(color, "RIGHT", upper_color)

        if en_passant_square == -1:
            return
        if en_passant_square == en_passant_target_left:
            moves_list.moves[moves_list.free_index] = Move(start_square, en_passant_target_left, piece,
                                                           SpecialFlags.EN_PASSANT.value)
            moves_list.free_index += 1
        elif en_passant_square == en_passant_target_right:
            moves_list.moves[moves_list.free_index] = Move(start_square, en_passant_target_right, piece,
                                                           SpecialFlags.EN_PASSANT.value)
            moves_list.free_index += 1

    @staticmethod
    def was_it_en_passant_move(move: Move, board: 'Board') -> bool:
        """
        Methods checks if it was an en passant move
        :param move: Move instance
        :param board: Board instance
        :return: bool
        """
        if move.get_moving_piece() != PiecesEnum.PAWN.value or board.get_fen_data().get_en_passant_square() == -1 or board.get_fen_data().get_en_passant_piece_square() == -1:
            return False
        return move.get_end_square() == board.get_fen_data().get_en_passant_square()

    @staticmethod
    def get_attack_direction(color: int, direction: str, upper_color: int) -> int:
        """
        Gets proper int direction of end_square
        :param upper_color: color of upper pieces
        :param color: int value of color
        :param direction: str attack direction
        :return: int
        """
        down_color: int = ColorManager.get_opposite_piece_color(upper_color)
        direct: str = direction.upper()
        pawn_direction_dict = {
            ("LEFT", down_color): MoveEnum.PAWN_UP_LEFT_ATTACK.value,
            ("RIGHT", down_color): MoveEnum.PAWN_UP_RIGHT_ATTACK.value,
            ("LEFT", upper_color): MoveEnum.PAWN_DOWN_LEFT_ATTACK.value,
            ("RIGHT", upper_color): MoveEnum.PAWN_DOWN_RIGHT_ATTACK.value
        }
        return pawn_direction_dict[direct, color]

    @staticmethod
    def is_pawn_promoting(move: Move, color: int, upper_color: int) -> bool:
        """
        Methods checks if pawn is promoting or not
        :param upper_color: color of upper pieces
        :param move: Move instance
        :param color: int value of color
        :return: bool
        """
        if move.get_moving_piece() != PiecesEnum.PAWN.value:
            return False
        if upper_color and 0 <= move.get_end_square() <= 7:
            return True
        
        opposite_color: int = ColorManager.get_opposite_piece_color(upper_color)
        return color == opposite_color and 57 <= move.get_end_square() <= 63
