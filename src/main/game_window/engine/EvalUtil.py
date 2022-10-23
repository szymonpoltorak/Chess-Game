from typing import TYPE_CHECKING

from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.Board import Board


class EvalUtil:
    @staticmethod
    def return_proper_evaluation_signed_value(board: 'Board', evaluation: int, favor_color: int) -> int:
        """
        Method used to return a proper mark of evaluation based on favor_color to move
        :param favor_color:
        :param board: Board instance
        :param evaluation: int value of evaluation
        :return: int value with proper sign
        """
        return evaluation if favor_color == board.get_engine_color() else -evaluation

    @staticmethod
    def is_queen_on_start_position(color: int, board: 'Board') -> bool:
        """
        Method used to check if queen is on starting position
        :param color: int vale of color
        :param board: Board instance
        :return: bool
        """
        start_positions = {
            board.get_engine_color(): 3,
            board.get_player_color(): 59
        }

        for square, piece in enumerate(board.get_board_array()):
            if piece == color | PiecesEnum.QUEEN.value and start_positions[color] == square:
                return True
        return False

    @staticmethod
    def get_piece_point_value(piece_value: int) -> int:
        """
        Method used to get proper eval value of a piece
        :param piece_value: int value of piece
        :return: int value of piece eval
        """
        pieces_dict = {
            PiecesEnum.KNIGHT.value: EvalEnum.KNIGHT.value,
            PiecesEnum.BISHOP.value: EvalEnum.BISHOP.value,
            PiecesEnum.ROOK.value: EvalEnum.ROOK.value,
            PiecesEnum.QUEEN.value: EvalEnum.QUEEN.value,
            PiecesEnum.PAWN.value: EvalEnum.PAWN.value,
            PiecesEnum.KING.value: EvalEnum.KING.value
        }
        return pieces_dict[piece_value]

    @staticmethod
    def is_it_free_line(board: 'Board', square: int, step: int, direction: int) -> bool:
        # TODO CHECK IF DISTANCES ARE BEING COUNTED RIGHT
        """
        Checks if given line is free of any piece
        :param board: Board instance
        :param square: rook position in array
        :param step: direction step
        :param direction: direction id in distances array
        :return: bool
        """
        second_direction: int = 4 if direction == 3 else 6
        board_array: ndarray[int] = board.get_board_array()
        distances: ndarray = board.get_distances()

        first_distance: int = distances[square][direction]
        first_border: int = first_distance * step + step

        second_distance: int = distances[square][second_direction]
        second_step: int = -step
        second_border: int = second_distance * second_step + second_step

        for index in range(square, first_border, step):
            if board_array[index] != PiecesEnum.NONE.value:
                return False

        for index in range(square, second_border, second_step):
            if board_array[index] != PiecesEnum.NONE.value:
                return False
        return True

    @staticmethod
    def is_friendly_pawn(board: 'Board', square: int, piece_color: int) -> bool:
        """
        Method used to check if piece is a pawn or not
        :param board: Board instance
        :param square: int value of square
        :param piece_color: int value of color
        :return: bool
        """
        piece: int = board.get_board_array()[square]
        current_piece_color: int = ColorManager.get_piece_color(piece)
        piece_value: int = piece - current_piece_color

        if piece_value != PiecesEnum.PAWN.value:
            return False
        return current_piece_color == piece_color

    @staticmethod
    def get_left_leaning_chain(board: 'Board', index: int, color: int, step_left: int) -> int:
        """
        Method used to get length of left chain
        :param board: Board instance
        :param index: index of current square
        :param color: int value of color
        :param step_left: int value of step of a left pawn move
        :return: int
        """
        if not EvalUtil.is_friendly_pawn(board, index, color):
            raise ValueError("IT SHOULD NOT HAPPEN!")

        chain_left_side = []
        working_index = index
        distances: ndarray[int] = board.get_distances()
        can_i_go_left = lambda square: distances[square][3] != 0
        can_i_go_right = lambda square: distances[square][4] != 0

        while can_i_go_left(working_index):
            working_index += step_left
            if working_index < 0 or working_index > 63:
                break
            if not EvalUtil.is_friendly_pawn(board, index, color):
                break
            chain_left_side.append(working_index)

        chain_right_side = []
        working_index = index

        while can_i_go_right(working_index):
            working_index += -step_left
            if working_index < 0 or working_index > 63:
                break
            if not EvalUtil.is_friendly_pawn(board, index, color):
                break
            chain_right_side.append(working_index)

        left_leaning_chain = chain_right_side + [index] + chain_left_side
        return len(left_leaning_chain)

    @staticmethod
    def get_right_leaning_chain(board: 'Board', index: int, color: int, step_right: int) -> int:
        """
        Method used to get length of right chain
        :param board: Board instance
        :param index: index of current square
        :param color: int value of color
        :param step_right: int value of step of a right pawn move
        :return: int
        """
        if not EvalUtil.is_friendly_pawn(board, index, color):
            raise ValueError("IT SHOULD NOT HAPPEN!")
        chain_right_side = []
        working_index = index

        distances: ndarray[int] = board.get_distances()
        can_i_go_left = lambda square: distances[square][3] != 0
        can_i_go_right = lambda square: distances[square][4] != 0

        while can_i_go_right(working_index):
            working_index += step_right
            if working_index < 0 or working_index > 63:
                break
            if not EvalUtil.is_friendly_pawn(board, index, color):
                break
            chain_right_side.append(working_index)

        chain_left_side = []
        working_index = index

        while can_i_go_left(working_index):
            working_index += -step_right
            if working_index < 0 or working_index > 63:
                break
            if not EvalUtil.is_friendly_pawn(board, index, color):
                break
            chain_left_side.append(working_index)

        right_leaning_chain = chain_right_side + [index] + chain_left_side

        return len(right_leaning_chain)

    @staticmethod
    def get_pawn_chains_eval(board: 'Board', color: int) -> int:
        """
        Method used to evaluate pawn chains for current color
        :param board: Board instance
        :param color: int value of color
        :return: int
        """
        step_left = -9 if color == board.get_player_color() else +7
        step_right = -7 if color == board.get_player_color() else +9

        chain_eval = 0

        for index in range(0, 64):
            if not EvalUtil.is_friendly_pawn(board, index, color):
                continue

            chain_eval += EvalUtil.get_left_leaning_chain(board, index, color, step_left)
            chain_eval += EvalUtil.get_right_leaning_chain(board, index, color, step_right)
        return chain_eval
