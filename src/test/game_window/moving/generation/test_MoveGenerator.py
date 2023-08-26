from src.main.game_window.board.Board import Board
from src.main.game_window.board.GameBoard import GameBoard
from src.main.game_window.board.fen.FenData import FenData
from src.main.game_window.board.fen.FenMaker import FenMaker
from src.main.game_window.enums.PiecesEnum import PiecesEnum
from src.main.game_window.moving.generation.MoveGenerator import MoveGenerator
from src.main.game_window.moving.generation.data.Move import Move
from src.main.game_window.moving.generation.data.MoveList import MoveList
from numpy import dtype
from numpy import int8
from numpy import ndarray


def test_generate_captures_only_no_capture_move() -> None:
    # given
    generator: MoveGenerator = MoveGenerator()
    expected: bool = True
    color: int = PiecesEnum.BLACK.value
    board: Board = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), generator)

    # when
    move_list: MoveList = generator.generate_legal_moves(color, board, captures_only=True)
    result: bool = move_list.is_empty()

    # then
    assert result == expected


def test_generate_captures_only_two_capture_moves() -> None:
    # given
    generator: MoveGenerator = MoveGenerator()
    expected: int = 2
    color: int = PiecesEnum.WHITE.value
    board: Board = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), generator)

    piece: int = board.delete_piece_from_board_square(59)
    board.delete_piece_from_board_square(51)

    board.add_piece_to_the_board(piece, 16)

    # when
    move_list: MoveList = generator.generate_legal_moves(color, board, captures_only=True)
    result: int = move_list.size()

    # then
    assert result == expected


def test_generate_captures_is_every_move_only_capture_for_sure() -> None:
    # given
    generator: MoveGenerator = MoveGenerator()
    expected: bool = True
    color: int = PiecesEnum.WHITE.value
    board: Board = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), generator)

    white_queen: int = board.delete_piece_from_board_square(59)
    black_queen: int = board.delete_piece_from_board_square(3)
    white_knight: int = board.delete_piece_from_board_square(62)
    black_knight: int = board.delete_piece_from_board_square(1)
    white_bishop: int = board.delete_piece_from_board_square(58)
    black_bishop: int = board.delete_piece_from_board_square(2)

    board.add_piece_to_the_board(white_queen, 34)
    board.add_piece_to_the_board(black_queen, 27)
    board.add_piece_to_the_board(white_knight, 35)
    board.add_piece_to_the_board(black_knight, 33)
    board.add_piece_to_the_board(white_bishop, 37)
    board.add_piece_to_the_board(black_bishop, 29)

    board_array: ndarray[int, dtype[int8]] = board.board_array()

    # when
    move_list: MoveList = generator.generate_legal_moves(color, board, captures_only=True)
    result: bool = True

    for index in range(move_list.size()):
        move: Move = move_list[index]

        if board_array[move.get_end_square()] == 0:
            result = False
            break

    # then
    assert result == expected
