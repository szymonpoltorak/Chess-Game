from game_window.board.Board import Board


def test_should_this_piece_move_white_color_piece_should_move():
    # given
    board = Board()
    expected = True
    row = 7
    col = 0

    # when
    result = board.should_this_piece_move(row, col)

    # then
    assert expected == result


def test_should_this_piece_move_black_color_piece_should_not_move():
    # given
    board = Board()
    expected = False
    row = 0
    col = 0

    # when
    result = board.should_this_piece_move(row, col)

    # then
    assert expected == result
