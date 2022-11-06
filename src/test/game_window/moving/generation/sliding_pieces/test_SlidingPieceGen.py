import pytest
from numpy import full

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.Board import Board
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.MoveList import MoveList
from game_window.moving.generation.sliding_piece.SlidingPiecesGen import SlidingPiecesGen


def test_is_sliding_piece_it_is():
    # given
    piece: int = PiecesEnum.QUEEN.value
    expected: bool = True

    # when
    result: bool = SlidingPiecesGen.is_sliding_piece(piece)

    # then
    assert expected == result


def test_is_sliding_piece_it_is_not():
    # given
    piece: int = PiecesEnum.KING.value
    expected : bool= False

    # when
    result: bool = SlidingPiecesGen.is_sliding_piece(piece)

    # then
    assert expected == result


def test_is_sliding_piece_null_piece():
    # given

    # when
    with pytest.raises(NullArgumentException):
        SlidingPiecesGen.is_sliding_piece(None)

    # then


def test_is_it_sliding_piece_move_bishop_not_diagonal_direction():
    # given
    piece: int = PiecesEnum.BISHOP.value
    expected: bool = False
    direction: int = MoveEnum.LEFT.value

    # when
    result: bool = SlidingPiecesGen.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_bishop_diagonal_direction():
    # given
    piece: int = PiecesEnum.BISHOP.value
    expected = True
    direction: int = MoveEnum.TOP_LEFT.value

    # when
    result: bool = SlidingPiecesGen.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_rook_diagonal_direction():
    # given
    piece: int = PiecesEnum.ROOK.value
    expected: bool = False
    direction: int = MoveEnum.TOP_LEFT.value

    # when
    result: bool = SlidingPiecesGen.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_rook_not_diagonal_direction():
    # given
    piece: int = PiecesEnum.ROOK.value
    direction: int = MoveEnum.LEFT.value
    expected: bool = True

    # when
    result: bool = SlidingPiecesGen.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_queen_not_diagonal_direction():
    # given
    piece: int = PiecesEnum.QUEEN.value
    expected: bool = True
    direction: int = MoveEnum.LEFT.value

    # when
    result: bool = SlidingPiecesGen.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_queen_diagonal_direction():
    # given
    piece: int = PiecesEnum.QUEEN.value
    expected: bool = True
    direction: int = MoveEnum.TOP_LEFT.value

    # when
    result: bool = SlidingPiecesGen.is_it_sliding_piece_move(piece, direction)

    # then
    assert expected == result


def test_is_it_sliding_piece_move_null_arguments():
    # given

    # when
    with pytest.raises(NullArgumentException):
        SlidingPiecesGen.is_it_sliding_piece_move(None, None)

    # then


def test_is_it_sliding_piece_move_not_sliding_piece():
    # given

    # when
    with pytest.raises(IllegalArgumentException):
        SlidingPiecesGen.is_it_sliding_piece_move(PiecesEnum.KING.value, MoveEnum.LEFT.value)

    # then


def test_is_it_sliding_piece_move_not_sliding_piece_direction():
    # given
    direction: int = 41

    # when
    with pytest.raises(IllegalArgumentException):
        SlidingPiecesGen.is_it_sliding_piece_move(PiecesEnum.QUEEN.value, direction)

    # then


def test_generate_sliding_piece_moves_not_sliding_piece():
    # given
    board: Board = Board()
    move_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)
    piece: int = PiecesEnum.KING.value
    color: int = PiecesEnum.BLACK.value
    start_square: int = 4

    # when
    with pytest.raises(IllegalArgumentException):
        SlidingPiecesGen.generate_sliding_piece_moves(piece, start_square, move_list, color, board)

    # then


def test_generate_sliding_piece_moves_empty_list():
    # given
    board: Board = Board()
    move_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)
    piece: int = PiecesEnum.BISHOP.value
    color: int = PiecesEnum.BLACK.value
    start_square: int = 4
    expected: bool = True

    # when
    SlidingPiecesGen.generate_sliding_piece_moves(piece, start_square, move_list, color, board)
    result: bool = move_list.is_empty()

    # then
    assert result == expected


def test_generate_sliding_piece_moves_null_args():
    # given

    # when
    with pytest.raises(NullArgumentException):
        SlidingPiecesGen.generate_sliding_piece_moves(None, None, None, None, None)

    # then


def test_generate_sliding_piece_moves_illegal_arguments():
    # given
    board: Board = Board()
    move_list: MoveList = MoveList(full(MoveEnum.MAX_NUM_OF_MOVES.value, None, dtype=object), 0)
    piece: int = -1
    color: int = 2
    start_square: int = -4

    # when
    with pytest.raises(IllegalArgumentException):
        SlidingPiecesGen.generate_sliding_piece_moves(piece, start_square, move_list, color, board)

    # then
