from functools import cache
from typing import TYPE_CHECKING

import numpy

from game_window.engine.Evaluator import Evaluator
from game_window.engine.MoveData import MoveData
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.Move import Move
from game_window.MoveGenerator import MoveGenerator
from game_window.MoveUtil import MoveUtil

if TYPE_CHECKING:
    from game_window.Board import Board


class Engine:
    @staticmethod
    @cache
    def search_positions(board: 'Board', depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
        if depth == 0:
            return Evaluator.evaluate_position(board)

        if maximizing_player:
            min_eval: int = numpy.inf
            moves: list[Move] = MoveGenerator.generate_legal_moves(board.get_player_color(), board)

            if not moves:
                return numpy.inf

            for move in moves:
                deleted_data: MoveData = MoveUtil.make_move(move, board.get_player_color(), board)
                board.set_opposite_move_color()
                movement_eval: int = Engine.search_positions(board, depth - 1, alpha, beta, False)
                MoveUtil.un_make_move(move, deleted_data.deleted_piece, board, deleted_data)

                min_eval: int = min(min_eval, movement_eval)
                beta: int = min(beta, movement_eval)

                if beta <= alpha:
                    break
            return min_eval
        elif not maximizing_player:
            max_eval: int = -numpy.inf
            moves: list[Move] = MoveGenerator.generate_legal_moves(board.get_engine_color(), board)

            if not moves:
                return -numpy.inf

            for move in moves:
                deleted_data: MoveData = MoveUtil.make_move(move, board.get_engine_color(), board)
                board.set_opposite_move_color()
                movement_eval: int = Engine.search_positions(board, depth - 1, alpha, beta, True)
                MoveUtil.un_make_move(move, deleted_data.deleted_piece, board, deleted_data)

                max_eval: int = max(max_eval, movement_eval)
                alpha: int = max(alpha, movement_eval)

                if beta <= alpha:
                    break
            return max_eval
        raise ValueError("WRONG PARAMETERS!")

    @staticmethod
    def get_computer_move(board: 'Board') -> Move:
        moves: list[Move] = MoveGenerator.generate_legal_moves(board.get_engine_color(), board)
        alpha: int = -numpy.inf
        beta: int = numpy.inf
        depth: int = 2
        best_eval: int = -numpy.inf
        best_move: Move or None = None

        for move in moves:
            if move.get_special_flag_value() == SpecialFlags.CASTLING.value:
                best_move = move
                break
            deleted_data: MoveData = MoveUtil.make_move(move, board.get_engine_color(), board)
            move_eval: int = Engine.search_positions(board, depth, alpha, beta, True)
            MoveUtil.un_make_move(move, deleted_data.deleted_piece, board, deleted_data)

            if move_eval > best_eval:
                best_move: Move or None = move
                best_eval: int = move_eval
        board.set_move_color(board.get_engine_color())
        return best_move
