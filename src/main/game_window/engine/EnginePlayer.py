from typing import TYPE_CHECKING

from numpy import inf

from game_window.ColorManager import ColorManager
from game_window.engine.Engine import Engine
from game_window.engine.Evaluation import Evaluation
from game_window.enums.MoveEnum import MoveEnum
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveData import MoveData
from game_window.moving.generation.data.MoveList import MoveList
from game_window.moving.generation.Generator import Generator
from game_window.moving.MoveMaker import MoveMaker

if TYPE_CHECKING:
    from game_window.board.Board import Board


class EnginePlayer(Engine):
    """
    Class containing methods to pick best __moves for computer
    """

    __slots__ = ("__generator", "__evaluator")

    def __init__(self, generator: Generator, evaluator: Evaluation) -> None:
        self.__generator: Generator = generator
        self.__evaluator: Evaluation = evaluator

    def get_computer_move(self, board: 'Board') -> Move:
        """
        Method used to return best computer move possible
        :param board: Board instance
        :return: the best computer Move instance
        """
        moves_list: MoveList = self.__generator.generate_legal_moves(board.engine_color(), board)
        depth: int = 5
        best_eval: float = -inf
        alpha: float = inf
        beta: float = -inf
        best_move: Move = Move(MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value)
        moves_list.sort(board)

        for index in range(moves_list.size()):
            move: Move = moves_list[index]

            deleted_data: MoveData = MoveMaker.make_move(move, board.engine_color(), board)
            evaluation: float = -self.__negamax_search(board, depth, alpha, beta, board.player_color())
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

        return best_move

    # def search_only_capture_moves(self, board: 'Board', color: int, alpha: float, beta: float) -> float:
    #     """
    #
    #     :param board:
    #     :param color:
    #     :param alpha:
    #     :param beta:
    #     :return:
    #     """
    #     start_eval: float = self.__evaluator.evaluate_position(board, color)
    #
    #     if start_eval >= beta:
    #         return beta
    #     alpha = max(alpha, start_eval)
    #     capture_moves: MoveList = self.__generator.generate_legal_moves(color, board, captures_only=True)
    #     capture_moves.sort(board)
    #
    #     for index in range(capture_moves.size()):
    #         move: Move = capture_moves[index]
    #         opposite_color: int = ColorManager.get_opposite_piece_color(color)
    #
    #         deleted_data: MoveData = MoveMaker.make_move(move, color, board)
    #         evaluation: float = -self.search_only_capture_moves(board, opposite_color, -beta, -alpha)
    #         MoveMaker.un_make_move(move, deleted_data, board)
    #
    #         if evaluation >= beta:
    #             return beta
    #         alpha = max(alpha, evaluation)
    #     return alpha

    def __negamax_search(self, board: 'Board', depth: int, alpha: float, beta: float, color: int) -> float:
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
            return self.__evaluator.evaluate_position(board, color)
        moves_list: MoveList = self.__generator.generate_legal_moves(color, board)

        if moves_list.is_empty():
            return -inf if color == board.engine_color() else inf
        evaluation: float = -inf
        moves_list.sort(board)

        for index in range(moves_list.size()):
            move: Move = moves_list[index]

            deleted_data: MoveData = MoveMaker.make_move(move, color, board)
            evaluation = max(evaluation, -self.__negamax_search(board, depth - 1, -beta, -alpha,
                                                                ColorManager.get_opposite_piece_color(color)))
            MoveMaker.un_make_move(move, deleted_data, board)

            alpha = max(alpha, evaluation)

            if alpha >= beta:
                break
        return evaluation
