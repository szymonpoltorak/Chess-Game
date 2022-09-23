from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move


class ValidateUtils:
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
            return MoveEnum.WHITE_ROOK_QUEEN.value
        elif is_queen_side and color == PiecesEnum.BLACK.value:
            return MoveEnum.BLACK_ROOK_QUEEN.value
        elif not is_queen_side and color == PiecesEnum.WHITE.value:
            return MoveEnum.WHITE_ROOK_KING.value
        elif not is_queen_side and color == PiecesEnum.BLACK.value:
            return MoveEnum.BLACK_ROOK_KING.value

    @staticmethod
    def disable_castling_on_side(color: int, move: Move, board) -> None:
        """
        Disable castling for king on given side
        :param color: int value of color
        :param move: Move instance
        :param board: Board instance
        :return: None
        """
        if color == PiecesEnum.BLACK.value and move.get_start_square() == MoveEnum.BLACK_ROOK_QUEEN.value:
            board.set_castling_queen_side(False, color)
        elif color == PiecesEnum.BLACK.value and move.get_start_square() == MoveEnum.BLACK_ROOK_KING.value:
            board.set_castling_king_side(False, color)
        elif color == PiecesEnum.WHITE.value and move.get_start_square() == MoveEnum.WHITE_ROOK_QUEEN.value:
            board.set_castling_queen_side(False, color)
        elif color == PiecesEnum.WHITE.value and move.get_start_square() == MoveEnum.WHITE_ROOK_KING.value:
            board.set_castling_king_side(False, color)

    @staticmethod
    def is_king_move_target_in_borders(start_square: int, move_target: int) -> bool:
        """
        Checks if move target square of king is in bonds of chess board.
        :param start_square: int index of start square
        :param move_target: int index of move target square
        :return: bool
        """
        start_col = start_square % BoardEnum.BOARD_LENGTH.value
        target_col = move_target % BoardEnum.BOARD_LENGTH.value

        if move_target > BoardEnum.BOARD_SIZE.value - 1 or move_target < 0:
            return False
        return abs(start_col - target_col) <= 1

    @staticmethod
    def is_knight_move_target_in_borders(start_square: int, move_target: int) -> bool:
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