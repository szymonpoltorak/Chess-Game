import multiprocessing

from numpy import inf

from src.main.game_window.ColorManager import ColorManager
from src.main.game_window.board.Board import Board
from src.main.game_window.engine.Engine import Engine
from src.main.game_window.engine.Evaluation import Evaluation
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.moving.MoveMaker import MoveMaker
from src.main.game_window.moving.generation.Generator import Generator
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.data.MoveData import MoveData
from src.main.game_window.moving.generation.data.MoveList import MoveList


class EnginePlayer(Engine):
    """
    Class containing methods to pick best __moves for computer
    """

    __slots__ = ("__generator", "__evaluator", "__board")

    def __init__(self, generator: Generator, evaluator: Evaluation) -> None:
        self.__generator: Generator = generator
        self.__evaluator: Evaluation = evaluator

    def get_computer_move(self, board: 'Board') -> Move:
        moves_list: MoveList = self.__generator.generate_legal_moves(board.engine_color(), board)
        best_eval: float = -inf
        alpha: float = -inf
        beta: float = inf
        best_move: Move = Move(MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value)
        moves_list.sort(board)

        num_processes = multiprocessing.cpu_count()
        print(f"NumOfProcesses : {num_processes}")
        pool = multiprocessing.Pool(processes=num_processes)

        results = []
        for index in range(moves_list.size()):
            move = moves_list[index]
            results.append(pool.apply_async(self.evaluate_move, (move, board.__copy__(), alpha, beta)))

        pool.close()
        pool.join()

        for result in results:
            move, evaluation = result.get()

            if evaluation > best_eval:
                best_move = move
                best_eval = evaluation

        return best_move

    def evaluate_move(self, move: Move, board: 'Board', alpha: float, beta: float):
        deleted_data = MoveMaker.make_move(move, board.engine_color(), board)
        evaluation = -self.__negamax_search(board, 3, -beta, -alpha, board.player_color())
        MoveMaker.un_make_move(move, deleted_data, board)
        return move, evaluation

    def __negamax_search(self, board: Board, depth: int, alpha: float, beta: float, favor_color: int) -> float:
        """
        Method used to evaluate positions and find possibly best move for engine
        :param board: Board instance
        :param depth: how deep computer should look through
        :param alpha: int value of alpha
        :param beta: int value of beta
        :param favor_color: int value of color which turn is now searched for
        :return: int value of best move evaluation
        """
        if depth == 0:
            return self.__evaluator.evaluate_position(board, favor_color)
        moves_list: MoveList = self.__generator.generate_legal_moves(color_to_move=favor_color, board=board)

        if moves_list.is_empty():
            return -inf
        evaluation: float = -inf

        moves_list.sort(board)

        for index in range(moves_list.size()):
            move: Move = moves_list[index]
            enemy_color: int = ColorManager.get_opposite_piece_color(favor_color)
            new_depth: int = depth - 1

            deleted_data: MoveData = MoveMaker.make_move(move=move, color=favor_color, board=board)
            evaluation = max(evaluation, -self.__negamax_search(board=board, depth=new_depth, alpha=-beta, beta=-alpha,
                                                                favor_color=enemy_color))
            MoveMaker.un_make_move(move=move, deleted_data=deleted_data, board=board)

            alpha = max(alpha, evaluation)

            if alpha >= beta:
                break
        return evaluation

    def __search_only_capture_moves(self, board: Board, color: int, alpha: float, beta: float) -> float:
        """

        :param board:
        :param color:
        :param alpha:
        :param beta:
        :return:
        """
        evaluation: float = self.__evaluator.evaluate_position(board, color)

        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)
        capture_moves: MoveList = self.__generator.generate_legal_moves(color_to_move=color, board=board,
                                                                              captures_only=True)
        if capture_moves.is_empty():
            return evaluation
        capture_moves.sort(board)

        for index in range(capture_moves.size()):
            move: Move = capture_moves[index]
            opposite_color: int = ColorManager.get_opposite_piece_color(color)

            deleted_data: MoveData = MoveMaker.make_move(move, color, board)
            evaluation = -self.__search_only_capture_moves(board=board, color=opposite_color, alpha=-beta, beta=-alpha)
            MoveMaker.un_make_move(move, deleted_data, board)

            if evaluation >= beta:
                return beta
            alpha = max(alpha, evaluation)
        return alpha
