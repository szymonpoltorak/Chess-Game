from typing import TYPE_CHECKING

from numpy import inf

from game_window.ColorManager import ColorManager
from game_window.engine.Evaluator import Evaluator
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveGenerator import MoveGenerator
from game_window.moving.MoveList import MoveList
from game_window.moving.MoveUtil import MoveUtil

if TYPE_CHECKING:
    from game_window.Board import Board


class Engine:
    @staticmethod
    def negamax_search(board: 'Board', depth: int, alpha: int, beta: int, color: int) -> int:
        if depth == 0:
            return Evaluator.evaluate_position(board, color)
        moves_list: MoveList = MoveGenerator.generate_legal_moves(color, board)

        if moves_list.moves[0] is None:
            return inf if color == board.get_engine_color() else -inf
        evaluation: int = -inf

        for move in moves_list.moves:
            if move is None:
                break
            deleted_data: MoveData = MoveUtil.make_move(move, color, board)
            evaluation: int = max(evaluation, -Engine.negamax_search(board, depth - 1, -beta, -alpha,
                                                                     ColorManager.get_opposite_piece_color(color)))
            MoveUtil.un_make_move(move, deleted_data, board)

            alpha = max(alpha, evaluation)

            if alpha >= beta:
                break
        return evaluation

    @staticmethod
    def get_computer_move(board: 'Board') -> Move:
        moves_list: MoveList = MoveGenerator.generate_legal_moves(board.get_engine_color(), board)
        depth: int = 2
        best_eval: int = -inf
        best_move: Move or None = None

        for move in moves_list.moves:
            if move is None:
                break

            deleted_data: MoveData = MoveUtil.make_move(move, board.get_engine_color(), board)
            evaluation: int = -Engine.negamax_search(board, depth, inf, -inf, board.get_player_color())
            MoveUtil.un_make_move(move, deleted_data, board)

            if evaluation > best_eval:
                best_move: Move or None = move
                best_eval: int = evaluation
        return best_move
