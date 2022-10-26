from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.sliding_piece.SlidingPiecesGen import SlidingPiecesGen


def test_is_sliding_piece_it_is():
    # given
    piece = PiecesEnum.QUEEN.value
    expected = True

    # when
    result = SlidingPiecesGen.is_sliding_piece(piece)

    # then
    assert expected == result


def test_is_sliding_piece_it_is_not():
    # given
    piece = PiecesEnum.KING.value
    expected = False

    # when
    result = SlidingPiecesGen.is_sliding_piece(piece)

    # then
    assert expected == result
