from typing import TYPE_CHECKING

from numpy import array
from numpy import int8
from numpy import ndarray
from numpy import zeros

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.FenData import FenData
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData

if TYPE_CHECKING:
    from game_window.Board import Board


class MoveUtil:
    __slots__ = ()

    @staticmethod
    def make_move(move: Move, color: int, board: 'Board') -> MoveData:
        # TODO PROMOTION MAY NOT WORK PROPERLY
        """
        Method used to make a given move. It means to update the board int array
        :param board: Board instance
        :param move: Move instance - move we want to make
        :param color: color of a piece
        :return:
        """
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        moving_piece: int = move.get_moving_piece()
        end_square: int = move.get_end_square()

        if board.get_board_array()[end_square] == color | PiecesEnum.ROOK.value:
            MoveUtil.disable_castling_on_side(color, end_square, board)
        if move.get_moving_piece() == PiecesEnum.ROOK.value:
            move_data: MoveData = MoveUtil.move_and_copy_move_data(board, move, color)
            MoveUtil.disable_castling_on_side(board.get_engine_color(), move.get_start_square(), board)

            return move_data
        elif special_flag == SpecialFlags.CASTLING.value:
            deleted_piece: int = color | moving_piece
            white_king, white_queen, black_king, black_queen, en_square, en_piece = fen_data.get_special_move_data()
            board.castle_king(deleted_piece, move)

            return MoveData(deleted_piece, white_king, white_queen, black_king, black_queen, en_square, en_piece)
        elif moving_piece == PiecesEnum.KING.value:
            move_data: MoveData = MoveUtil.move_and_copy_move_data(board, move, color)
            fen_data.set_castling_king_side(False, board.get_engine_color())
            fen_data.set_castling_queen_side(False, board.get_engine_color())

            return move_data
        else:
            return MoveUtil.move_and_copy_move_data(board, move, color)

    @staticmethod
    def un_make_move(move: Move, deleted_data: MoveData, board: 'Board') -> None:
        # TODO PROMOTION MAY NOT WORK PROPERLY
        """
        Removes given move with a value of deleted piece
        :param deleted_data: MoveData instance
        :param board: Board instance
        :param move: move to be unmade
        :return: None
        """
        end_square: int = move.get_end_square()
        start_square: int = move.get_start_square()
        board_array: ndarray[int] = board.get_board_array()
        special_flag: int = move.get_special_flag_value()
        fen_data: FenData = board.get_fen_data()
        deleted_piece = deleted_data.deleted_piece
        color: int = ColorManager.get_piece_color(deleted_piece)

        if special_flag == SpecialFlags.CASTLING.value:
            board.un_castle_king(move, color)
            fen_data.update_fen_data(deleted_data)
        else:
            fen_data.update_fen_data(deleted_data)
            moved_piece: int = board_array[end_square]
            board_array[end_square] = deleted_piece
            board_array[start_square] = moved_piece

    @staticmethod
    def move_and_copy_move_data(board: 'Board', move: Move, color: int) -> MoveData:
        """
        Method used to copy move data and making a move
        :param board: Board instance
        :param move: Move instance
        :param color: int value of color
        :return: MoveData instance
        """
        board_array: ndarray[int] = board.get_board_array()
        fen_data: FenData = board.get_fen_data()
        end_square: int = move.get_end_square()
        white_king, white_queen, black_king, black_queen, en_square, en_piece = fen_data.get_special_move_data()

        deleted_piece: int = board_array[end_square]
        board_array[move.get_start_square()] = 0
        board_array[end_square] = color + move.get_moving_piece()

        return MoveData(deleted_piece, white_king, white_queen, black_king, black_queen, en_square, en_piece)

    @staticmethod
    def is_it_a_promotion(special_flag: int) -> bool:
        """
        Checks if it is a promotion
        :param special_flag: int value of a special flag
        :return: bool
        """
        promotions: ndarray[int] = array([SpecialFlags.PROMOTE_TO_ROOK.value, SpecialFlags.PROMOTE_TO_QUEEN.value,
                                          SpecialFlags.PROMOTE_TO_BISHOP.value, SpecialFlags.PROMOTE_TO_KNIGHT.value])
        return special_flag in promotions

    @staticmethod
    def update_no_sack_and_pawn_counter(fen_data: FenData, deleted_piece: int, moving_piece: int) -> None:
        """
        Method used to update no sack and pawn move counter
        :param fen_data: FenData instance
        :param deleted_piece: int value of a piece
        :param moving_piece: int value of a moving piece
        :return: None
        """
        if deleted_piece != 0 or moving_piece == PiecesEnum.PAWN.value:
            fen_data.update_no_sack_and_pawn_count(True)
        elif deleted_piece == 0 or moving_piece != PiecesEnum.PAWN.value:
            fen_data.update_no_sack_and_pawn_count(False)
        else:
            raise ValueError("NOT POSSIBLE CONDITION OCCURRED! WRONG PARAMETERS")

    @staticmethod
    def disable_castling_on_side(color: int, target_square: int, board: 'Board') -> None:
        """
        Disable castling for king on given side
        :param target_square:
        :param color: int value of color
        :param board: Board instance
        :return: None
        """
        fen_data: FenData = board.get_fen_data()

        if target_square in (MoveEnum.TOP_ROOK_QUEEN.value, MoveEnum.BOTTOM_ROOK_QUEEN.value):
            fen_data.set_castling_queen_side(False, color)
        elif target_square in (MoveEnum.TOP_ROOK_KING.value, MoveEnum.BOTTOM_ROOK_KING.value):
            fen_data.set_castling_king_side(False, color)

    @staticmethod
    def disable_castling_if_deleted_rook(deleted_piece: int, color: int, square: int, board: 'Board') -> None:
        """
        Method used to disable castling if rook was captured
        :param deleted_piece: int value of deleted piece
        :param color: int value of friendly color
        :param square: int index of rook square
        :param board: Board instance
        :return: None
        """
        if deleted_piece == ColorManager.get_opposite_piece_color(color) | PiecesEnum.ROOK.value:
            MoveUtil.disable_castling_on_side(ColorManager.get_opposite_piece_color(color), square, board)

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
    def is_it_free_vertical_line(board: 'Board', square: int) -> bool:
        """
        Method used to check lanes if there is any piece on the way of rook in vertical orientation
        :param board:
        :param square:
        :return:
        """
        top_direction = 1
        bottom_direction: int = 6
        board_array: ndarray[int] = board.get_board_array()
        distances: ndarray = board.get_distances()

        distance_to_top: int = distances[square][top_direction]
        top_step: int = 8
        top_border: int = distance_to_top * top_step + top_step

        distance_to_bottom: int = distances[square][bottom_direction]
        down_step: int = -8
        bottom_border: int = distance_to_bottom * down_step + down_step

        for index in range(square, top_border, top_step):
            if board_array[index] != PiecesEnum.NONE.value:
                return False

        for index in range(square, bottom_border, down_step):
            if board_array[index] != PiecesEnum.NONE.value:
                return False
        return True

    @staticmethod
    def is_it_free_horizontal_line(board: 'Board', square: int) -> bool:
        """
        Method used to check lanes if there is any piece on the way of rook in horizontal orientation
        :param board:
        :param square:
        :return:
        """
        left_direction = 3
        right_direction: int = 4
        board_array: ndarray[int] = board.get_board_array()
        distances: ndarray = board.get_distances()

        distance_to_left: int = distances[square][left_direction]
        left_step: int = -1
        left_border: int = distance_to_left * left_step + left_step

        distance_to_right: int = distances[square][right_direction]
        right_step: int = 1
        right_border: int = distance_to_right * right_step + right_step

        for index in range(square, left_border, left_step):
            if board_array[index] != PiecesEnum.NONE.value:
                return False

        for index in range(square, right_border, right_step):
            if board_array[index] != PiecesEnum.NONE.value:
                return False
        return True
