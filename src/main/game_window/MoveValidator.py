from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move


class MoveValidator:
    @staticmethod
    def is_anything_on_king_side(board, start_square: int, color: int) -> bool:
        """
        Checks if there is anything on the path between a king side rook and the king
        :param board: Board instance
        :param start_square: int index of kings square
        :param color: int value of color
        :return: bool
        """
        for square in range(1, MoveEnum.KING_SIDE.value + 1):
            distance = start_square + square
            if color == PiecesEnum.BLACK.value and distance > 7 or color == PiecesEnum.WHITE.value and distance > 63:
                return True
            if board.get_board_array()[distance] != 0:
                return True
        return False

    @staticmethod
    def is_anything_on_queen_side(board, start_square: int) -> bool:
        """
        Checks if there is anything on the path between a queen side rook and the king
        :param board: Board instance
        :param start_square: int index of kings square
        :return: bool
        """
        square = abs(MoveEnum.QUEEN_SIDE.value)

        while square > 0:
            if board.get_board_array()[start_square - square] != 0:
                return True
            square -= 1
        return False

    @staticmethod
    def is_it_castling(move: Move) -> bool:
        """
        Checks if this move is castling
        :param move: Move instance
        :return: bool
        """
        move_length = abs(move.get_end_square() - move.get_start_square())

        return move.get_moving_piece() == PiecesEnum.KING.value and move_length == MoveEnum.CASTLE_MOVE.value

    @staticmethod
    def get_rook_position(color: int, is_queen_side: bool) -> int:
        """
        Static method to return rooks board position based on given parameters
        :param color: rook color
        :param is_queen_side: bool
        :return: int value of rook position
        """
        if is_queen_side and color == PiecesEnum.WHITE.value:
            return MoveEnum.BOTTOM_ROOK_QUEEN.value
        elif is_queen_side and color == PiecesEnum.BLACK.value:
            return MoveEnum.TOP_ROOK_QUEEN.value
        elif not is_queen_side and color == PiecesEnum.WHITE.value:
            return MoveEnum.BOTTOM_ROOK_KING.value
        elif not is_queen_side and color == PiecesEnum.BLACK.value:
            return MoveEnum.TOP_ROOK_KING.value

    @staticmethod
    def disable_castling_on_side(color: int, move: Move, board) -> None:
        """
        Disable castling for king on given side
        :param color: int value of color
        :param move: Move instance
        :param board: Board instance
        :return: None
        """
        if color == PiecesEnum.BLACK.value and move.get_start_square() == MoveEnum.TOP_ROOK_QUEEN.value:
            board.set_castling_queen_side(False, color)
        elif color == PiecesEnum.BLACK.value and move.get_start_square() == MoveEnum.TOP_ROOK_KING.value:
            board.set_castling_king_side(False, color)
        elif color == PiecesEnum.WHITE.value and move.get_start_square() == MoveEnum.BOTTOM_ROOK_QUEEN.value:
            board.set_castling_queen_side(False, color)
        elif color == PiecesEnum.WHITE.value and move.get_start_square() == MoveEnum.BOTTOM_ROOK_KING.value:
            board.set_castling_king_side(False, color)

    @staticmethod
    def is_attack_target_in_border_bounds(start_square: int, move_target: int, attack_range: int) -> bool:
        """
        Static method to check if pawns attack target is in board bonds
        :param start_square: int index of start square
        :param move_target: int index of attack target square
        :param attack_range: int value of range attack
        :return: bool
        """
        start_col = start_square % BoardEnum.BOARD_LENGTH.value
        target_col = move_target % BoardEnum.BOARD_LENGTH.value

        return abs(start_col - target_col) <= attack_range

    @staticmethod
    def is_it_sliding_piece(piece: int, direction: int) -> bool:
        """
        Static method used to check if this move should be calculated
        :param piece: int value of piece_square
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
        Static method used to check if piece_square is a sliding piece_square.
        :param piece: int value of piece_square
        :return: bool value of if piece_square is sliding piece_square or not
        """
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)

    @staticmethod
    def add_pawn_moves(start_square: int, piece: int, color: int, moves: list[Move], board) -> None:
        """
        Adds possible pawn movements
        :param start_square: int index of starting square
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param moves: list of moves
        :param board: Board instance
        :return: None
        """
        if color == PiecesEnum.WHITE.value:
            double_move_target = start_square + MoveEnum.PAWN_UP_DOUBLE_MOVE.value
            move_target = start_square + MoveEnum.PAWN_UP_SINGLE_MOVE.value

            if double_move_target < 0 or move_target < 0:
                return

            if 48 <= start_square <= 55 and MoveValidator.no_piece_in_pawns_way(double_move_target, start_square, board,
                                                                                MoveEnum.PAWN_UP_SINGLE_MOVE.value):
                moves.append(Move(start_square, double_move_target, piece))
            if board.get_board_array()[move_target] == 0:
                moves.append(Move(start_square, move_target, piece))
        else:
            double_move_target = start_square + MoveEnum.PAWN_DOWN_DOUBLE_MOVE.value
            move_target = start_square + MoveEnum.PAWN_DOWN_SINGLE_MOVE.value

            if double_move_target > 63 or move_target > 63:
                return

            if 8 <= start_square <= 15 and MoveValidator.no_piece_in_pawns_way(double_move_target, start_square, board,
                                                                               MoveEnum.PAWN_DOWN_SINGLE_MOVE.value):
                moves.append(Move(start_square, double_move_target, piece))
            if board.get_board_array()[move_target] == 0:
                moves.append(Move(start_square, move_target, piece))

    @staticmethod
    def no_piece_in_pawns_way(double_move_target: int, start_square: int, board, step: int) -> bool:
        """
        Static method used to check if there is any piece_square on pawns way
        :param double_move_target: int target square of pawns double move
        :param start_square: int index of starting square
        :param board: Board instance
        :param step: int value of step
        :return: bool
        """
        piece_single_up = board.get_board_array()[start_square + step]
        piece_double_up = board.get_board_array()[double_move_target]

        return piece_double_up == 0 and piece_single_up == 0

    @staticmethod
    def add_pawn_attacks(start_square: int, piece: int, color: int, moves: list[Move], board) -> None:
        """
        Static method used to add pawn attacks
        :param start_square: int index of starting square
        :param piece: int value of a piece_square
        :param color: int value of color to move
        :param moves: list of moves
        :param board: Board instance
        :return: None
        """
        left_piece_square = start_square + MoveValidator.get_attack_direction(color, "LEFT")
        right_piece_square = start_square + MoveValidator.get_attack_direction(color, "RIGHT")

        if left_piece_square < 0 or left_piece_square > 63 or right_piece_square < 0 or right_piece_square > 63:
            return
        left_piece = board.get_board_array()[left_piece_square]
        right_piece = board.get_board_array()[right_piece_square]

        if color != ColorManager.get_piece_color(left_piece) and left_piece != PiecesEnum.NONE.value:
            if MoveValidator.is_attack_target_in_border_bounds(start_square, left_piece_square, MoveEnum.PAWN_RANGE.value):
                moves.append(Move(start_square, left_piece_square, piece))
        if color != ColorManager.get_piece_color(right_piece) and right_piece != PiecesEnum.NONE.value:
            if MoveValidator.is_attack_target_in_border_bounds(start_square, right_piece_square, MoveEnum.PAWN_RANGE.value):
                moves.append(Move(start_square, right_piece_square, piece))
        MoveValidator.check_en_passant_movement(start_square, piece, color, moves, board)

    @staticmethod
    def check_en_passant_movement(start_square: int, piece: int, color: int, moves: list[Move], board):
        en_passant_square = board.get_en_passant_square()
        en_passant_target_left = start_square + MoveValidator.get_attack_direction(color, "LEFT")
        en_passant_target_right = start_square + MoveValidator.get_attack_direction(color, "RIGHT")

        if en_passant_square == -1:
            return
        if en_passant_square == en_passant_target_left:
            moves.append(Move(start_square, en_passant_target_left, piece))
        elif en_passant_square == en_passant_target_right:
            moves.append(Move(start_square, en_passant_target_right, piece))

    @staticmethod
    def was_it_en_passant_move(move: Move, board):
        if move.get_moving_piece() != PiecesEnum.PAWN.value or board.get_en_passant_square() == -1 or board.get_en_passant_piece_square() == -1:
            return False
        return move.get_end_square() == board.get_en_passant_square()

    @staticmethod
    def get_attack_direction(color: int, direction: str) -> int:
        """
        Gets proper int direction of square
        :param color: int value of color
        :param direction: str attack direction
        :return: int
        """
        if direction.upper() == "LEFT" and color == PiecesEnum.WHITE.value:
            return MoveEnum.PAWN_UP_LEFT_ATTACK.value
        elif direction.upper() == "RIGHT" and color == PiecesEnum.WHITE.value:
            return MoveEnum.PAWN_UP_RIGHT_ATTACK.value
        elif direction.upper() == "LEFT" and color == PiecesEnum.BLACK.value:
            return MoveEnum.PAWN_DOWN_LEFT_ATTACK.value
        elif direction.upper() == "RIGHT" and color == PiecesEnum.BLACK.value:
            return MoveEnum.PAWN_DOWN_RIGHT_ATTACK.value

    @staticmethod
    def is_pawn_promoting(move: Move, color: int) -> bool:
        if move.get_moving_piece() != PiecesEnum.PAWN.value:
            return False
        if color == PiecesEnum.WHITE.value and 0 <= move.get_end_square() <= 7:
            return True
        return color == PiecesEnum.BLACK.value and 57 <= move.get_end_square() <= 63
