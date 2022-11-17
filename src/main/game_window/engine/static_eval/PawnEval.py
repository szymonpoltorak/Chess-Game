from typing import TYPE_CHECKING

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.board.Board import Board


class PawnEval:
    """
    Class containing methods to evaluate pawns
    """

    __slots__ = ()

    @staticmethod
    def evaluate_pawn_chains(board: 'Board', favor_color: int) -> float:
        """
        Method used to evaluate pawn chains on board
        :param board: Board instance
        :param favor_color: int value of color
        :return: float
        """
        enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)

        favor_eval: float = PawnEval.get_pawn_chains_eval(board, favor_color)
        enemy_eval: float = PawnEval.get_pawn_chains_eval(board, enemy_color)

        evaluation: float = favor_eval - enemy_eval

        return evaluation

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
        working_index: int = index
        distances: ndarray[int, dtype[int8]] = board.get_distances()

        while distances[working_index][3] != 0:
            working_index += step_left

            if working_index < 0 or working_index > 63 or not PawnEval.is_friendly_pawn(board, working_index, color):
                break
            chain_left_side.append(working_index)
        chain_right_side = []
        working_index = index

        while distances[working_index][4] != 0:
            working_index += -step_left

            if working_index < 0 or working_index > 63 or not PawnEval.is_friendly_pawn(board, working_index, color):
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
        working_index: int = index
        distances: ndarray[int, dtype[int8]] = board.get_distances()

        while distances[working_index][4] != 0:
            working_index += step_right

            if working_index < 0 or working_index > 63 or not PawnEval.is_friendly_pawn(board, working_index, color):
                break
            chain_right_side.append(working_index)
        chain_left_side = []
        working_index = index

        while distances[working_index][3] != 0:
            working_index -= step_right

            if working_index < 0 or working_index > 63 or not PawnEval.is_friendly_pawn(board, working_index, color):
                break
            chain_left_side.append(working_index)
        right_leaning_chain = chain_right_side + [index] + chain_left_side

        return len(right_leaning_chain)

    @staticmethod
    def get_pawn_chains_eval(board: 'Board', color: int) -> float:
        """
        Method used to evaluate pawn chains for current color
        :param board: Board instance
        :param color: int value of color
        :return: float
        """
        step_left = MoveEnum.TOP_LEFT.value if color == board.get_player_color() else MoveEnum.BOTTOM_LEFT.value
        step_right = MoveEnum.TOP_RIGHT.value if color == board.get_player_color() else MoveEnum.BOTTOM_RIGHT.value
        chain_eval: int = 0

        for index in range(BoardEnum.BOARD_SIZE.value):
            if not PawnEval.is_friendly_pawn(board, index, color):
                continue

            chain_eval += PawnEval.get_left_leaning_chain(board, index, color, step_left)
            chain_eval += PawnEval.get_right_leaning_chain(board, index, color, step_right)
        return chain_eval
