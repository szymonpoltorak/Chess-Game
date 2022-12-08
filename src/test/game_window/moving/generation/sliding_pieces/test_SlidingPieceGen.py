import pytest
from numpy import full

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.board.GameBoard import GameBoard
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.data.Moves import Moves
from game_window.moving.generation.MoveGenerator import MoveGenerator
from game_window.moving.generation.sliding_piece.SlidingGenerator import SlidingGenerator
from game_window.moving.generation.sliding_piece.SlidingPiecesGen import SlidingPiecesGen


def test_generate_sliding_piece_moves_not_sliding_piece() -> None:
    # given
    sliding_gen: SlidingGenerator = SlidingPiecesGen()
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    move_list: Moves = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)
    piece: int = PiecesEnum.KING.value
    color: int = PiecesEnum.BLACK.value
    start_square: int = 4

    # when
    with pytest.raises(IllegalArgumentException):
        sliding_gen.generate_sliding_piece_moves(piece, start_square, move_list, color, board, False)

    # then


def test_generate_sliding_piece_moves_empty_list() -> None:
    # given
    sliding_gen: SlidingGenerator = SlidingPiecesGen()
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    move_list: Moves = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)
    piece: int = PiecesEnum.BISHOP.value
    color: int = PiecesEnum.BLACK.value
    start_square: int = 4
    expected: bool = True

    # when
    sliding_gen.generate_sliding_piece_moves(piece, start_square, move_list, color, board, False)
    result: bool = move_list.is_empty()

    # then
    assert result == expected


def test_generate_sliding_piece_moves_null_args() -> None:
    # given
    sliding_gen: SlidingGenerator = SlidingPiecesGen()

    # when
    with pytest.raises(NullArgumentException):
        sliding_gen.generate_sliding_piece_moves(None, None, None, None, None, False)

    # then


def test_generate_sliding_piece_moves_illegal_arguments() -> None:
    # given
    sliding_gen: SlidingGenerator = SlidingPiecesGen()
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    move_list: Moves = Moves(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)
    piece: int = -1
    color: int = 2
    start_square: int = -4

    # when
    with pytest.raises(IllegalArgumentException):
        sliding_gen.generate_sliding_piece_moves(piece, start_square, move_list, color, board, False)

    # then
