from typing import TYPE_CHECKING

import numpy

from game_window.engine.Evaluator import Evaluator
from game_window.engine.MadeMove import MadeMove
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.Move import Move
from game_window.MoveGenerator import MoveGenerator
from game_window.MoveUtil import MoveUtil

if TYPE_CHECKING:
    from game_window.Board import Board


class Engine:
    @staticmethod
    def search_positions(board: 'Board', depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
        if depth == 0:
            return Evaluator.evaluate_position(board)

        if maximizing_player:
            min_eval: int = numpy.inf
            moves: list[Move] = MoveGenerator.generate_legal_moves(PiecesEnum.WHITE.value, board)

            if not moves:
                return numpy.inf

            for move in moves:
                deleted_data: MadeMove = MoveUtil.make_move(move, PiecesEnum.WHITE.value, board.get_board_array())
                movement_eval: int = Engine.search_positions(board, depth - 1, alpha, beta, False)
                Engine.unmake_move_properly(deleted_data, move, board)

                min_eval: int = min(min_eval, movement_eval)
                beta: int = min(beta, movement_eval)

                if beta <= alpha:
                    break
            return min_eval
        elif not maximizing_player:
            max_eval: int = -numpy.inf
            moves: list[Move] = MoveGenerator.generate_legal_moves(PiecesEnum.BLACK.value, board)

            if not moves:
                return -numpy.inf

            for move in moves:
                deleted_data: MadeMove = MoveUtil.make_move(move, PiecesEnum.BLACK.value, board.get_board_array(),
                                                            fen_data=board.get_fen_data())
                movement_eval: int = Engine.search_positions(board, depth - 1, alpha, beta, True)
                Engine.unmake_move_properly(deleted_data, move, board)

                max_eval: int = max(max_eval, movement_eval)
                alpha: int = max(alpha, movement_eval)

                if beta <= alpha:
                    break
            return max_eval
        raise ValueError("WRONG PARAMETERS!")

    @staticmethod
    def unmake_move_properly(deleted_data: MadeMove, move: Move, board: 'Board'):
        may_none_elements = (deleted_data.en_passant_square, deleted_data.en_passant_piece_square,
                             deleted_data.black_castle_queen, deleted_data.black_castle_king,
                             deleted_data.white_castle_king, deleted_data.white_castle_queen)
        if deleted_data.deleted_piece is None:
            raise ValueError("DELETED PIECE CANNOT BE NULL!")
        if None not in may_none_elements:
            MoveUtil.un_make_move(move, deleted_data.deleted_piece, board.get_board_array(),
                                  fen_data=board.get_fen_data(), prev_data=deleted_data)
        MoveUtil.un_make_move(move, deleted_data.deleted_piece, board.get_board_array())

    @staticmethod
    def get_computer_move(board: 'Board') -> Move:
        moves: list[Move] = MoveGenerator.generate_legal_moves(board.get_engine_color(), board)
        alpha: int = -numpy.inf
        beta: int = numpy.inf
        depth: int = 2
        best_eval: int = -numpy.inf
        best_move: Move or None = None

        for move in moves:
            deleted_data: MadeMove = MoveUtil.make_move(move, board.get_engine_color(), board.get_board_array())
            move_eval: int = Engine.search_positions(board, depth, alpha, beta, True)
            Engine.unmake_move_properly(deleted_data, move, board)

            if move_eval > best_eval:
                best_move: Move or None = move
                best_eval: int = move_eval
        return best_move
