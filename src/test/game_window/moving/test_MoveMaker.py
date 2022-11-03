from typing import Tuple

from numpy import dtype
from numpy import int8
from numpy import ndarray

from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.moving.Move import Move
from game_window.moving.MoveData import MoveData
from game_window.moving.MoveMaker import MoveMaker


def test_make_move():
    # given
    board: Board = Board()
    expected: int = PiecesEnum.BLACK.value | PiecesEnum.ROOK.value
    color: int = PiecesEnum.WHITE.value
    start_square: int = 63
    end_square: int = 0
    move: Move = Move(start_square, end_square, PiecesEnum.ROOK.value, SpecialFlags.NONE.value)

    # when
    result: MoveData = MoveMaker.make_move(move, color, board)

    # then
    assert expected == result.deleted_piece


def test_un_make_move():
    # given
    board = Board()
    expected: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_piece: int = PiecesEnum.WHITE.value | PiecesEnum.ROOK.value
    deleted_data: MoveData = MoveData(deleted_piece, MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value,
                                      MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value)
    start_square: int = 63
    end_square: int = 0
    move: Move = Move(start_square, end_square, PiecesEnum.ROOK.value, SpecialFlags.NONE.value)

    # when
    MoveMaker.un_make_move(move, deleted_data, board)
    result: int = board.get_board_array()[end_square]

    # then
    assert expected == result


def test_make_castling_move_king_side():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    color: int = PiecesEnum.WHITE.value
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    rook_pos: int = 61
    king_pos: int = 62
    expected: Tuple[int, int] = (color | PiecesEnum.ROOK.value, color | PiecesEnum.KING.value)

    board.delete_pieces_on_squares(61, 62)

    # when
    MoveMaker.make_move(move, color, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_un_make_castling_move_king_side():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    color: int = PiecesEnum.WHITE.value
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    rook_pos: int = 61
    king_pos: int = 62
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.NONE.value)

    board.delete_pieces_on_squares(61, 62)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, color, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_does_making_move_return_proper_move_data():
    # given
    board: Board = Board()
    move: Move = Move(60, 62, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected: MoveData = MoveData(PiecesEnum.WHITE.value | PiecesEnum.KING.value, True, True, True, True,
                                  MoveEnum.NONE.value, MoveEnum.NONE.value)

    board.delete_pieces_on_squares(61, 62)

    # when
    result: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)

    # then
    assert result == expected


def test_make_castling_move_queen_side():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    color: int = PiecesEnum.WHITE.value
    rook_pos: int = 59
    king_pos: int = 58
    move: Move = Move(60, king_pos, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected: Tuple[int, int] = (color | PiecesEnum.ROOK.value, color | PiecesEnum.KING.value)

    board.delete_piece_from_board(6, 0)
    board.delete_pieces_on_squares(58, 59)

    # when
    MoveMaker.make_move(move, color, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_un_make_castling_move_queen_side():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    color: int = PiecesEnum.WHITE.value
    rook_pos: int = 59
    king_pos: int = 58
    move: Move = Move(60, king_pos, PiecesEnum.KING.value, SpecialFlags.CASTLING.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.NONE.value)

    board.delete_piece_from_board(6, 0)
    board.delete_pieces_on_squares(58, 59)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, color, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[rook_pos], board_array[king_pos])

    # then
    assert result == expected


def test_make_left_en_passant_move():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    fen_data: FenData = board.get_fen_data()
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.PAWN.value)
    captured_pawn_pos: int = 27
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 19
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_pieces_on_squares(52, capturing_pawn_pos)
    board.delete_pieces_on_squares(11, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)

    fen_data.set_en_passant_square(en_passant_pos)
    fen_data.set_en_passant_piece_square(captured_pawn_pos)
    board.update_fen()

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos])

    # then
    assert result == expected


def test_un_make_left_en_passant_move():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: Tuple[int, int] = (PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)
    captured_pawn_pos: int = 27
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 19
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_pieces_on_squares(52, capturing_pawn_pos)
    board.delete_pieces_on_squares(11, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)
    board.update_fen()

    fen_data.set_en_passant_square(en_passant_pos)
    fen_data.set_en_passant_piece_square(captured_pawn_pos)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos])

    # then
    assert result == expected


def test_make_right_en_passant_move():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    fen_data: FenData = board.get_fen_data()
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.PAWN.value)
    captured_pawn_pos: int = 29
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 21
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_pieces_on_squares(52, capturing_pawn_pos)
    board.delete_pieces_on_squares(13, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)

    fen_data.set_en_passant_square(en_passant_pos)
    fen_data.set_en_passant_piece_square(captured_pawn_pos)
    board.update_fen()

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos])

    # then
    assert result == expected


def test_un_make_right_en_passant_move():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    fen_data: FenData = FenData(PiecesEnum.WHITE.value)
    expected: Tuple[int, int] = (PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)
    captured_pawn_pos: int = 29
    capturing_pawn_pos: int = 28
    en_passant_pos: int = 21
    move: Move = Move(capturing_pawn_pos, en_passant_pos, PiecesEnum.PAWN.value, SpecialFlags.EN_PASSANT.value)

    board.delete_pieces_on_squares(52, capturing_pawn_pos)
    board.delete_pieces_on_squares(13, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.BLACK.value | PiecesEnum.PAWN.value, captured_pawn_pos)
    board.add_piece_to_the_board(PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, capturing_pawn_pos)
    board.update_fen()

    fen_data.set_en_passant_square(en_passant_pos)
    fen_data.set_en_passant_piece_square(captured_pawn_pos)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[captured_pawn_pos], board_array[en_passant_pos])

    # then
    assert result == expected


def test_make_promotion_to_queen():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_QUEEN.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.QUEEN.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_queen():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_QUEEN.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_promotion_to_rook():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.ROOK.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_rook():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_promotion_to_bishop():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_BISHOP.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.BISHOP.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_bishop():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_BISHOP.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_promotion_to_knight():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_KNIGHT.value)
    expected: Tuple[int, int] = (PiecesEnum.NONE.value, PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_un_make_promotion_to_knight():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 8
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_KNIGHT.value)
    expected: Tuple[int, int] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value, PiecesEnum.NONE.value)

    board.delete_pieces_on_squares(48, 8)
    board.delete_piece_from_board(0, 0)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    result: Tuple[int, int] = (board_array[promotion_start_square], board_array[promotion_end_square])

    # then
    assert result == expected


def test_make_capture_of_rook():
    # given
    board: Board = Board()
    promotion_start_square: int = 9
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: bool = False

    board.delete_pieces_on_squares(49, 9)

    # when
    MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    result: bool = board.get_fen_data().can_king_castle_queen_side(PiecesEnum.BLACK.value)

    # then
    assert result == expected


def test_un_make_capture_of_rook():
    # given
    board: Board = Board()
    board_array: ndarray[int, dtype[int8]] = board.get_board_array()
    promotion_start_square: int = 9
    promotion_end_square: int = 0
    move: Move = Move(promotion_start_square, promotion_end_square, PiecesEnum.PAWN.value,
                      SpecialFlags.PROMOTE_TO_ROOK.value)
    expected: Tuple[int, int, bool] = (PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                                       PiecesEnum.BLACK.value | PiecesEnum.ROOK.value, True)

    board.delete_pieces_on_squares(49, 9)

    # when
    deleted_data: MoveData = MoveMaker.make_move(move, PiecesEnum.WHITE.value, board)
    MoveMaker.un_make_move(move, deleted_data, board)
    can_castle: bool = board.get_fen_data().can_king_castle_queen_side(PiecesEnum.BLACK.value)
    result: Tuple[int, int, bool] = (board_array[promotion_start_square], board_array[promotion_end_square], can_castle)

    # then
    assert result == expected

