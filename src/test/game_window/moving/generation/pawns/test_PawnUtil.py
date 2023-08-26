import pytest
from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.board.GameBoard import GameBoard
from src.main.game_window.board.fen.FenData import FenData
from src.main.game_window.board.fen.FenMaker import FenMaker
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.enums.SpecialFlags import SpecialFlags
from src.main.game_window.moving.generation.MoveGenerator import MoveGenerator
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.pawns.PawnUtil import PawnUtil


def test_get_attack_direction_left_white() -> None:
    # given
    expected: int = -9
    direction: str = "LEFT"
    color: int = PiecesEnum.WHITE.value

    # when
    result: int = PawnUtil.get_attack_direction(color, direction, PiecesEnum.BLACK.value)

    # then
    assert expected == result


def test_get_attack_direction_right_black() -> None:
    # given
    expected: int = 9
    direction: str = "RIGHT"
    color: int = PiecesEnum.BLACK.value

    # when
    result: int = PawnUtil.get_attack_direction(color, direction, PiecesEnum.BLACK.value)

    # then
    assert expected == result


def test_get_attack_direction_null_args() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        PawnUtil.get_attack_direction(None, None, None)

    # then


def test_get_attack_direction_illegal_colors() -> None:
    # given
    color: int = 0
    engine_color: int = 7
    direction: str = "LEFT"

    # when
    with pytest.raises(IllegalArgumentException):
        PawnUtil.get_attack_direction(color, direction, engine_color)

    # then


def test_get_attack_direction_illegal_direction() -> None:
    # given
    color: int = 8
    engine_color: int = 16
    direction: str = "TOP"

    # when
    with pytest.raises(IllegalArgumentException):
        PawnUtil.get_attack_direction(color, direction, engine_color)

    # then


def test_is_pawn_promoting_white_pawn_is_promoting() -> None:
    # given
    start_square: int = 8
    end_square: int = 0
    color: int = PiecesEnum.WHITE.value
    move: Move = Move(start_square, end_square, PiecesEnum.PAWN.value, SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: bool = True

    # when
    result: bool = PawnUtil.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_it_is_not_pawn() -> None:
    # given
    start_square: int = 8
    end_square: int = 0
    color: int = PiecesEnum.WHITE.value
    move: Move = Move(start_square, end_square, PiecesEnum.QUEEN.value, SpecialFlags.NONE.value)
    expected: bool = False

    # when
    result: bool = PawnUtil.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_black_pawn_is_promoting() -> None:
    # given
    start_square: int = 56
    end_square: int = 63
    color: int = PiecesEnum.BLACK.value
    move: Move = Move(start_square, end_square, PiecesEnum.PAWN.value, SpecialFlags.PROMOTE_TO_QUEEN.value)
    expected: bool = True

    # when
    result: bool = PawnUtil.is_pawn_promoting(move, color, PiecesEnum.WHITE.value)

    # then
    assert expected == result


def test_is_pawn_promoting_null_args() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        PawnUtil.is_pawn_promoting(None, None, None)

    # then


def test_is_pawn_promoting_illegal_colors() -> None:
    # given
    move: Move = Move(50, 42, PiecesEnum.PAWN.value, SpecialFlags.NONE.value)
    color: int = 0
    engine_color: int = 9

    # when
    with pytest.raises(IllegalArgumentException):
        PawnUtil.is_pawn_promoting(move, color, engine_color)

    # then


def test_was_it_en_passant_move_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        PawnUtil.was_it_en_passant_move(None, None)

    # then


def test_no_piece_in_pawns_way_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        PawnUtil.no_piece_in_pawns_way(None, None, None, None)

    # then


def test_no_piece_in_pawns_way_illegal_args() -> None:
    # given
    double_move_target: int = -1
    start_square: int = 52
    step: int = -8
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())

    # when
    with pytest.raises(IllegalArgumentException):
        PawnUtil.no_piece_in_pawns_way(double_move_target, start_square, board, step)

    # then


def test_no_piece_in_pawns_way_proper_use() -> None:
    # given
    double_move_target: int = 36
    start_square: int = 52
    step: int = -8
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())
    expected: bool = True

    # when
    result: bool = PawnUtil.no_piece_in_pawns_way(double_move_target, start_square, board, step)

    # then
    assert result == expected


def test_is_it_a_promotion_null_flag() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        PawnUtil.is_it_a_promotion(None)

    # then


def test_is_it_a_promotion_it_is_promotion() -> None:
    # given
    expected: bool = True

    # when
    result: bool = PawnUtil.is_it_a_promotion(SpecialFlags.PROMOTE_TO_QUEEN.value)

    # then
    assert result == expected


def test_is_attack_target_in_border_bounds_nulls() -> None:
    # given

    # when
    with pytest.raises(NullArgumentException):
        PawnUtil.is_attack_target_in_border_bounds(None, None, None)

    # then


def test_is_attack_target_in_border_bounds_squares_out_of_bonds() -> None:
    # given

    # when
    with pytest.raises(IllegalArgumentException):
        PawnUtil.is_attack_target_in_border_bounds(-1, 64, 8)

    # then
