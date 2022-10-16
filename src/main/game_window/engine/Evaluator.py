import math
from typing import TYPE_CHECKING

from numpy import array
from numpy import int8
from numpy import ndarray

from game_window.CheckUtil import CheckUtil
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.EvalEnum import EvalEnum
from game_window.enums.PiecesEnum import PiecesEnum

if TYPE_CHECKING:
    from game_window.Board import Board


class Evaluator:
    @staticmethod
    def evaluate_position(board: 'Board') -> int:
        evaluation: int = 7 * Evaluator.sum_pieces_on_board(board)
        evaluation += 2.5 * Evaluator.evaluate_center_possession(board)
        evaluation += 4 * Evaluator.evaluate_light_pieces_walked(board)
        evaluation += Evaluator.evaluate_distance_to_enemy_king(board)

        return evaluation

    @staticmethod
    def sum_pieces_on_board(board: 'Board') -> int:
        evaluation: int = 0
        board_array: ndarray[int] = board.get_board_array()

        for square in board_array:
            color: int = ColorManager.get_piece_color(board_array[square])
            piece_value: int = board_array[square] - color
            points: int = Evaluator.get_piece_point_value(piece_value)
            evaluation += points if color == board.get_engine_color() else -points

        return Evaluator.return_proper_evaluation_signed_value(board, evaluation)

    @staticmethod
    def evaluate_light_pieces_walked(board: 'Board'):
        light_starting_positions: dict = {
            board.get_engine_color(): array([1, 2, 5, 6], dtype=int8),
            board.get_player_color(): array([56, 57, 61, 62], dtype=int8)
        }
        light_pieces: ndarray[int] = array([PiecesEnum.KNIGHT.value, PiecesEnum.BISHOP.value])
        board_array: ndarray[int] = board.get_board_array()
        evaluation: int = 0

        for position in light_starting_positions[board.get_engine_color()]:
            color: int = ColorManager.get_piece_color(board_array[position])

            if board_array[position] - color not in light_pieces and color == board.get_engine_color():
                evaluation -= EvalEnum.WALKED.value

        for position in light_starting_positions[board.get_player_color()]:
            color: int = ColorManager.get_piece_color(board_array[position])

            if board_array[position] - color not in light_pieces and color == board.get_player_color():
                evaluation += EvalEnum.WALKED.value
        return Evaluator.return_proper_evaluation_signed_value(board, evaluation)

    @staticmethod
    def evaluate_distance_to_enemy_king(board: 'Board'):
        our_color: int = board.get_color_to_move()
        enemy_color: int = ColorManager.get_opposite_piece_color(our_color)

        board_array: ndarray[int] = board.get_board_array()

        enemy_king_pos = CheckUtil.find_friendly_king_squares(board_array, enemy_color)
        enemy_king_x = math.floor(enemy_king_pos / 8)
        enemy_king_y = enemy_king_pos - 8 * enemy_king_x

        score_accumulator = 0

        for pos in range(BoardEnum.BOARD_SIZE.value):
            if ColorManager.get_piece_color(board_array[pos]) != our_color:
                continue

            my_piece_x = math.floor(pos / 8)
            my_piece_y = my_piece_x - 8 * pos

            x_diff = enemy_king_x - my_piece_x
            y_diff = enemy_king_y - my_piece_y

            distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
            score = 8 * math.sqrt(2) - distance
            score_accumulator += score

        return Evaluator.return_proper_evaluation_signed_value(board, score_accumulator)

    @staticmethod
    def return_proper_evaluation_signed_value(board: 'Board', evaluation: int):
        return evaluation if board.get_color_to_move() == board.get_engine_color() else -evaluation

    @staticmethod
    def get_piece_point_value(piece_value: int) -> int:
        pieces_dict = {
            PiecesEnum.NONE.value: PiecesEnum.NONE.value,
            PiecesEnum.KNIGHT.value: EvalEnum.KNIGHT.value,
            PiecesEnum.BISHOP.value: EvalEnum.BISHOP.value,
            PiecesEnum.ROOK.value: EvalEnum.ROOK.value,
            PiecesEnum.QUEEN.value: EvalEnum.QUEEN.value,
            PiecesEnum.PAWN.value: EvalEnum.PAWN.value,
            PiecesEnum.KING.value: EvalEnum.KING.value
        }
        return pieces_dict[piece_value]

    @staticmethod
    def evaluate_center_possession(board: 'Board'):
        evaluation: int = 0
        board_array: ndarray[int] = board.get_board_array()

        for center_square in range(26, 30):
            if board_array[center_square] == PiecesEnum.NONE.value:
                continue
            color: int = ColorManager.get_piece_color(board_array[center_square])
            evaluation += EvalEnum.CENTER.value if color == board.get_engine_color() else -EvalEnum.CENTER.value

        for center_square in range(34, 38):
            if board_array[center_square] == PiecesEnum.NONE.value:
                continue
            color: int = ColorManager.get_piece_color(board_array[center_square])
            evaluation += EvalEnum.CENTER.value if color == board.get_engine_color() else -EvalEnum.CENTER.value
        return evaluation if board.get_color_to_move() == board.get_engine_color() else -evaluation
