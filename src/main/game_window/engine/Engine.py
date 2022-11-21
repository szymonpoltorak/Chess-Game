from typing import TYPE_CHECKING

from numpy import inf

from game_window.ColorManager import ColorManager
from game_window.engine.Evaluator import Evaluator
from game_window.enums.MoveEnum import MoveEnum
from game_window.moving.generation.MoveGenerator import MoveGenerator
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveList import MoveList
from game_window.moving.MoveMaker import MoveMaker

if TYPE_CHECKING:
    from game_window.board.Board import Board


class Engine:
    """
    Class containing methods to pick best __moves for computer
    """

    @staticmethod
    def negamax_search(board: 'Board', depth: int, alpha: float, beta: float, color: int) -> float:
        """
        Method used to evaluate positions and find possibly best move for engine
        :param board: Board instance
        :param depth: how deep computer should look through
        :param alpha: int value of alpha
        :param beta: int value of beta
        :param color: int value of color which turn is now searched for
        :return: int value of best move evaluation
        """
        if depth == 0:
            return Evaluator.evaluate_position(board, color)
        moves_list: MoveList = MoveGenerator.generate_legal_moves(color, board)

        if moves_list.is_empty():
            return -inf if color == board.get_engine_color() else inf
        evaluation: float = -inf
        moves_list.sort(board)

        for move in moves_list:
            if move is None:
                break
            deleted_data: MoveData = MoveMaker.make_move(move, color, board)
            evaluation = max(evaluation, -Engine.negamax_search(board, depth - 1, -beta, -alpha,
                                                                ColorManager.get_opposite_piece_color(color)))
            MoveMaker.un_make_move(move, deleted_data, board)

            alpha = max(alpha, evaluation)

            if alpha >= beta:
                break
        return evaluation

    @staticmethod
    def get_computer_move(board: 'Board') -> Move:
        """
        Method used to return best computer move possible
        :param board: Board instance
        :return: the best computer Move instance
        """
        moves_list: MoveList = MoveGenerator.generate_legal_moves(board.get_engine_color(), board)
        depth: int = 5
        best_eval: float = -inf
        alpha: float = inf
        beta: float = -inf
        best_move: Move = Move(MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value)
        moves_list.sort(board)

        for move in moves_list:
            if move is None:
                break

            deleted_data: MoveData = MoveMaker.make_move(move, board.get_engine_color(), board)
            evaluation: float = -Engine.negamax_search(board, depth, alpha, beta, board.get_player_color())
            MoveMaker.un_make_move(move, deleted_data, board)
            print("-----------------------------------------------------------------")
            print(f"BestEval : {best_eval}\nEvaluation : {evaluation}\n")
            print(f"Current Move : \n{move}")
            print("-----------------------------------------------------------------")

            if evaluation > best_eval:
                best_move = move
                best_eval = evaluation
        print("-----------------------------------------------------------------")
        print(f"Best Eval : {best_eval}\nBest Move : \n{best_move}\n")
        print("-----------------------------------------------------------------")

        return best_move if best_eval != -inf else None
