from typing import TYPE_CHECKING

from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.engine.static_eval.StaticEvalUtil import StaticEvalUtil
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.Board import Board


class PawnEval:
    @staticmethod
    def evaluate_pawn_chains(board: 'Board', favor_color: int) -> int:
        """
        Method used to evaluate pawn chains on board
        :param board: Board instance
        :param favor_color: int value of color
        :return: int
        """
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)

        favor_eval: int = PawnEval.get_pawn_chains_eval(board, favor_color)
        enemy_eval: int = PawnEval.get_pawn_chains_eval(board, enemy_color)

        evaluation: int = favor_eval - enemy_eval

        return StaticEvalUtil.return_proper_evaluation_signed_value(board, evaluation, favor_color)

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
        if not PawnEval.is_friendly_pawn(board, index, color):
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
            if not PawnEval.is_friendly_pawn(board, index, color):
                break
            chain_left_side.append(working_index)

        chain_right_side = []
        working_index = index

        while can_i_go_right(working_index):
            working_index += -step_left

            if working_index < 0 or working_index > 63:
                break
            if not PawnEval.is_friendly_pawn(board, index, color):
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
        if not PawnEval.is_friendly_pawn(board, index, color):
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
            if not PawnEval.is_friendly_pawn(board, index, color):
                break
            chain_right_side.append(working_index)
        chain_left_side = []
        working_index = index

        while can_i_go_left(working_index):
            working_index += -step_right

            if working_index < 0 or working_index > 63:
                break
            if not PawnEval.is_friendly_pawn(board, index, color):
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
        step_left = -9 if color == board.get_player_color() else 7
        step_right = -7 if color == board.get_player_color() else 9

        chain_eval = 0

        for index in range(0, 64):
            if not PawnEval.is_friendly_pawn(board, index, color):
                continue

            chain_eval += PawnEval.get_left_leaning_chain(board, index, color, step_left)
            chain_eval += PawnEval.get_right_leaning_chain(board, index, color, step_right)
        return chain_eval
