import pytest

from exceptions.IllegalArgumentException import IllegalArgumentException
from exceptions.NullArgumentException import NullArgumentException
from game_window.board.GameBoard import GameBoard
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenMaker import FenMaker
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.MoveGenerator import MoveGenerator
from game_window.PromotionData import PromotionData


def test_check_user_choice_null_args() -> None:
    # given
    promotion_data: PromotionData = PromotionData()

    # when
    with pytest.raises(NullArgumentException):
        promotion_data.check_user_choice(None, None, None, None)

    # then


def test_check_user_choice_arguments_are_negatives() -> None:
    # given
    promotion_data: PromotionData = PromotionData()
    rect_size: int = -1
    y: int = -2
    x: int = -3
    board: GameBoard = GameBoard(FenMaker(FenData(PiecesEnum.WHITE.value)), MoveGenerator())

    # when
    with pytest.raises(IllegalArgumentException):
        promotion_data.check_user_choice(rect_size, board, x, y)

    # then
