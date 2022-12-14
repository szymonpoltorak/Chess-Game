import pytest
from numpy import array
from numpy import dtype
from numpy import int8
from numpy import ndarray
from numpy import zeros

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.board.GameBoard import GameBoard
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.MoveGenerator import MoveGenerator


def test_find_friendly_king_squares_only_enemy_king() -> None:
    # given
    color_to_move: int = PiecesEnum.WHITE.value
    board_array: ndarray[int, dtype[int8]] = zeros(BoardEnum.BOARD_SIZE.value)
    board_array[30] = PiecesEnum.BLACK.value | PiecesEnum.KING.value

    # when
    with pytest.raises(ValueError):
        result = KingUtil.find_friendly_king_squares(board_array, color_to_move)

    # then


def test_find_friendly_king_squares_a_friendly_king() -> None:
    # given
    color_to_move: int = PiecesEnum.BLACK.value
    board_array: ndarray[int, dtype[int8]] = zeros(BoardEnum.BOARD_SIZE.value)
    index: int = 30
    board_array[index] = PiecesEnum.BLACK.value | PiecesEnum.KING.value
    expected: int = index

    # when
    result: int = KingUtil.find_friendly_king_squares(board_array, color_to_move)

    # then
    assert expected == result


def test_get_castling_squares_move_distance_greater_than_0() -> None:
    # given
    start_square: int = 4
    end_square: int = 6
    piece: int = PiecesEnum.KING.value
    move: Move = Move(start_square, end_square, piece, SpecialFlags.CASTLING.value)
    expected: ndarray[int, dtype[int8]] = array([start_square, start_square + 1, start_square + 2])

    # when
    result: ndarray[int, dtype[int8]] = KingUtil.get_castling_squares(move)

    # then
    assert expected.all() == result.all()


def test_get_castling_squares_move_distance_less_than_0() -> None:
    # given
    start_square: int = 6
    end_square: int = 4
    piece: int = PiecesEnum.KING.value
    move: Move = Move(start_square, end_square, piece, SpecialFlags.CASTLING.value)
    expected: ndarray[int, dtype[int8]] = array([start_square, start_square - 1, start_square - 2])

    # when
    result: ndarray[int, dtype[int8]] = KingUtil.get_castling_squares(move)

    # then
    assert expected.all() == result.all()


def test_is_anything_on_king_side_start_square_out_of_bonds() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    start_square: int = -4

    # when
    with pytest.raises(IllegalArgumentException):
        result: bool = KingUtil.is_anything_on_king_side(board, start_square)

    # then


def test_is_anything_on_king_side_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: bool = KingUtil.is_anything_on_king_side(None, None)

    # then


def test_is_anything_on_king_side_it_is() -> None:
    # given
    expected: bool = True
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    start_square: int = 60

    # when
    result: bool = KingUtil.is_anything_on_king_side(board, start_square)

    # then
    assert result == expected


def test_is_anything_on_king_side_it_is_not() -> None:
    # given
    expected: bool = False
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    start_square: int = 60

    board.delete_piece_from_board_square(start_square + 1)
    board.delete_piece_from_board_square(start_square + 2)

    # when
    result: bool = KingUtil.is_anything_on_king_side(board, start_square)

    # then
    assert result == expected


def test_is_anything_on_queen_side_it_is() -> None:
    # given
    expected: bool = True
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    start_square: int = 60

    # when
    result: bool = KingUtil.is_anything_on_queen_side(board, start_square)

    # then
    assert result == expected


def test_is_anything_on_queen_side_it_is_not() -> None:
    # given
    expected: bool = False
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    start_square: int = 60

    board.delete_piece_from_board_square(start_square - 1)
    board.delete_piece_from_board_square(start_square - 2)
    board.delete_piece_from_board_square(start_square - 3)

    # when
    result: bool = KingUtil.is_anything_on_queen_side(board, start_square)

    # then
    assert result == expected


def test_is_anything_on_queen_side_start_square_out_of_bonds() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    start_square: int = -4

    # when
    with pytest.raises(IllegalArgumentException):
        result: bool = KingUtil.is_anything_on_queen_side(board, start_square)

    # then


def test_is_anything_on_queen_side_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: bool = KingUtil.is_anything_on_queen_side(None, None)

    # then


def test_check_castling_squares_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: bool = KingUtil.check_castling_squares(None, None, None, None)

    # then


def test_check_castling_squares_square_out_of_bonds() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())

    # when
    with pytest.raises(IllegalArgumentException):
        result: bool = KingUtil.check_castling_squares(1, 8, -1, board)

    # then


def test_find_friendly_king_squares_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: int = KingUtil.find_friendly_king_squares(None, None)

    # then


def test_find_friendly_king_squares_out_of_bonds() -> None:
    # given
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())

    # when
    with pytest.raises(IllegalArgumentException):
        result: int = KingUtil.find_friendly_king_squares(board.board_array(), -3)

    # then


def test_get_castling_squares_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: ndarray[int, dtype[int8]] = KingUtil.get_castling_squares(None)

    # then


def test_is_it_castling_null_move() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: bool = KingUtil.is_it_castling(None)

    # then


def test_is_it_castling_castling_move() -> None:
    # given
    expected: bool = True
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)

    # when
    result: bool = KingUtil.is_it_castling(move)

    # then
    assert result == expected


def test_is_it_castling_not_castling_move() -> None:
    # given
    expected: bool = False
    move: Move = Move(60, 61, PiecesEnum.KING.value, -1)

    # when
    result: bool = KingUtil.is_it_castling(move)

    # then
    assert result == expected


def test_is_it_castling_not_a_king() -> None:
    # given
    expected: bool = False
    move: Move = Move(60, 61, PiecesEnum.PAWN.value, -1)

    # when
    result: bool = KingUtil.is_it_castling(move)

    # then
    assert result == expected


def test_get_rook_position_null_args() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        result: int = KingUtil.get_rook_position(None, None, None, None)

    # then


def test_get_rook_position_invalid_colors() -> None:
    # given
    color: int = 15
    engine_color: int = 9
    player_color: int = 8
    is_queen_side: bool = True

    # when
    with pytest.raises(IllegalArgumentException):
        result: int = KingUtil.get_rook_position(color, is_queen_side, engine_color, player_color)

    # then


def test_get_rook_position_queen_side() -> None:
    # given
    color: int = PiecesEnum.BLACK.value
    engine_color: int = PiecesEnum.BLACK.value
    player_color: int = PiecesEnum.WHITE.value
    is_queen_side: bool = True
    expected: int = 0

    # when
    result: int = KingUtil.get_rook_position(color, is_queen_side, engine_color, player_color)

    # then
    assert result == expected


def test_get_rook_position_king_side() -> None:
    # given
    color: int = PiecesEnum.BLACK.value
    engine_color: int = PiecesEnum.BLACK.value
    player_color: int = PiecesEnum.WHITE.value
    is_queen_side: bool = False
    expected: int = 7

    # when
    result: int = KingUtil.get_rook_position(color, is_queen_side, engine_color, player_color)

    # then
    assert result == expected
