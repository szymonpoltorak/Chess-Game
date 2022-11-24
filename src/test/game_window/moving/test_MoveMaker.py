from typing import Tuple

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.generation.data.Move import Move
from game_window.moving.generation.data.MoveData import MoveData
from game_window.moving.MoveMaker import MoveMaker


def test_make_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: int = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    color: int = PiecesEnum.WHITE.value
    start_square: int = 63
    end_square: int = 0
    move: Move = Move(start_square, end_square, PiecesEnum.ROOK.value, SpecialFlags.NONE.value)

    # when
    result: MoveData = MoveMaker.make_move(move, color, board)

    # then
    assert expected == result.deleted_piece


def test_un_make_move() -> None:
    # given
    board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    expected: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_piece: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_data: MoveData = MoveData(deleted_piece, MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value,
                                      MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value,
                                      MoveEnum.NONE.value, MoveEnum.NONE.value)
    start_square: int = 63
    end_square: int = 0
    move: Move = Move(start_square, end_square, PiecesEnum.ROOK.value, SpecialFlags.NONE.value)

    # when
    MoveMaker.un_make_move(move, deleted_data, board)
    result: int = board.board_array()[end_square]

    # then
    assert expected == result


def test_make_castling_move_king_side() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    color: int = PiecesEnum.WHITE.value
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    rook_pos: int = 61
    king_pos: int = 62
    expected: Tuple[int, int] = (color | PiecesEnum.ROOK.value, color | PiecesEnum.KING.value)

    board.delete_piece_from_board_square(61)
    board.delete_piece_from_board_square(62)

    # when
    MoveMaker.make_move(move, color, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_un_make_castling_move_king_side() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    color: int = PiecesEnum.WHITE.value
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    rook_pos: int = 61
    king_pos: int = 62
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board_square(61)
    board.delete_piece_from_board_square(62)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, color, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_does_making_move_return_proper_move_data() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected: MoveData = MoveData(PiecesEnum.WHITE.value | PiecesEnum.KING.value, True, True, True, True,
                                  MoveEnum.NONE.value, MoveEnum.NONE.value, 0, 0)

    board.delete_piece_from_board_square(61)
    board.delete_piece_from_board_square(62)

    # when
    result: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)

    # then
    assert result == expected


def test_make_castling_move_queen_side() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    color: int = PiecesEnum.WHITE.value
    rook_pos: int = 59
    king_pos: int = 58
    move: Move = Move(60, king_pos, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected: Tuple[int, int] = (color | PiecesEnum.ROOK.value, color | PiecesEnum.KING.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(58)
    board.delete_piece_from_board_square(59)

    # when
    MoveMaker.make_move(move, color, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_un_make_castling_move_queen_side() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    color: int = PiecesEnum.WHITE.value
    rook_pos: int = 59
    king_pos: int = 58
    move: Move = Move(60, king_pos, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(58)
    board.delete_piece_from_board_square(59)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, color, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_make_left_en_passant_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    expected: Tuple[int, int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                                      PiecesEnum.NONE.value)
    captured_pawn_pos: int = 27
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 19
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_piece_from_board_square(52)
    board.delete_piece_from_board_square(11)
    board.delete_piece_from_board_square(capturing_pawn_pos)
    board.delete_piece_from_board_square(captured_pawn_pos)

    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)

    board.set_en_passant_square(en_passant_pos)
    board.set_en_passant_piece_square(captured_pawn_pos)
    board.update_fen()

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos],
                                    board_array[capturing_pawn_pos])

    # then
    assert result == expected
    assert board.en_passant_square() == -1
    assert board.en_passant_piece_square() == -1


def test_un_make_left_en_passant_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    expected: Tuple[int, int, int] = (PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value,
                                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value)
    captured_pawn_pos: int = 27
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 19
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_piece_from_board_square(52)
    board.delete_piece_from_board_square(11)
    board.delete_piece_from_board_square(capturing_pawn_pos)
    board.delete_piece_from_board_square(captured_pawn_pos)

    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)

    board.set_en_passant_square(en_passant_pos)
    board.set_en_passant_piece_square(captured_pawn_pos)
    board.update_fen()

    # when
    move_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, move_data, board)
    result: Tuple[int, int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos],
                                    board_array[capturing_pawn_pos])

    # then
    assert result == expected
    assert board.en_passant_square() == en_passant_pos
    assert board.en_passant_piece_square() == captured_pawn_pos


def test_make_right_en_passant_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    expected: Tuple[int, int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                                      PiecesEnum.NONE.value)
    captured_pawn_pos: int = 29
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 21
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_piece_from_board_square(52)
    board.delete_piece_from_board_square(11)
    board.delete_piece_from_board_square(capturing_pawn_pos)
    board.delete_piece_from_board_square(captured_pawn_pos)

    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)

    board.set_en_passant_square(en_passant_pos)
    board.set_en_passant_piece_square(captured_pawn_pos)
    board.update_fen()

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos],
                                    board_array[capturing_pawn_pos])

    # then
    assert result == expected
    assert board.en_passant_square() == -1
    assert board.en_passant_piece_square() == -1


def test_un_make_right_en_passant_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    expected: Tuple[int, int, int] = (PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value,
                                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value)
    captured_pawn_pos: int = 29
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 21
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_piece_from_board_square(52)
    board.delete_piece_from_board_square(11)
    board.delete_piece_from_board_square(capturing_pawn_pos)
    board.delete_piece_from_board_square(captured_pawn_pos)

    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)

    board.set_en_passant_square(en_passant_pos)
    board.set_en_passant_piece_square(captured_pawn_pos)
    board.update_fen()

    # when
    move_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, move_data, board)
    result: Tuple[int, int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos],
                                    board_array[capturing_pawn_pos])

    # then
    assert result == expected
    assert board.en_passant_square() == en_passant_pos
    assert board.en_passant_piece_square() == captured_pawn_pos


def test_make_promotion_to_queen() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_QUEEN.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.QUEEN.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_queen() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_QUEEN.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_promotion_to_rook() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.ROOK.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_rook() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_promotion_to_bishop() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_BISHOP.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.BISHOP.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_bishop() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_BISHOP.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_promotion_to_knight() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_KNIGHT.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_knight() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_KNIGHT.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board_square(48)
    board.delete_piece_from_board_square(8)
    board.delete_piece_from_board_square(0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_capture_of_rook() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    promotion_start_square: int = 9
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: bool = False

    board.delete_piece_from_board_square(49)
    board.delete_piece_from_board_square(9)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: bool = board.can_king_castle_queen_side(PiecesEnum.BLACK.value)

    # then
    assert result == expected


def test_un_make_capture_of_rook() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    board_array: ndarray[int, dtype[int8]] = board.board_array()
    promotion_start_square: int = 9
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: Tuple[int, int, bool] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                                       PiecesEnum.BLACK.value | PiecesEnum.ROOK.value, True)

    board.delete_piece_from_board_square(49)
    board.delete_piece_from_board_square(9)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    can_castle: bool = board.can_king_castle_queen_side(PiecesEnum.BLACK.value)
    result: Tuple[int, int, bool] = (board_array[promotion_start_square], board_array[promotion_end_square], can_castle)

    # then
    assert result == expected


def test_make_double_pawn_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    move: Move = Move(48, 32, PiecesEnum.PAWN.value, SpecialFlags.NONE.value)
    color: int = PiecesEnum.WHITE.value
    expected: Tuple[int, int, int] = (color | PiecesEnum.PAWN.value, 40, 32)

    # when
    MoveMaker.make_move(move, color, board)

    en_square: int = board.en_passant_square()
    en_piece_square: int = board.en_passant_piece_square()
    result: Tuple[int, int, int] = (board.board_array()[32], en_square, en_piece_square)

    # then
    assert result == expected


def test_un_make_double_pawn_move() -> None:
    # given
    board: Board = Board(FenMaker(FenData(PiecesEnum.WHITE.value)))
    move: Move = Move(48, 32, PiecesEnum.PAWN.value, SpecialFlags.NONE.value)
    color: int = PiecesEnum.WHITE.value
    expected: Tuple[int, int, int] = (0, -1, -1)
    start_string = board.fen_string()

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, color, board)
    MoveMaker.un_make_move(move, deleted_data, board)

    en_square: int = board.en_passant_square()
    en_piece_square: int = board.en_passant_piece_square()
    result: Tuple[int, int, int] = (board.board_array()[32], en_square, en_piece_square)

    # then
    assert result == expected
    assert start_string == board.fen_string()
