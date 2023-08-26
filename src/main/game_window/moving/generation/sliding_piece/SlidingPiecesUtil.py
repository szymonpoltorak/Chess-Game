from src.main.exceptions.IllegalArgumentException import IllegalArgumentException
from src.main.exceptions.NullArgumentException import NullArgumentException
from src.main.game_window.enums.MoveEnum import MoveEnum
from src.main.game_window.enums.PiecesEnum import PiecesEnum


class SlidingPiecesUtil:
    """
    Util class for sliding pieces generation
    """

    __slots__ = ()

    @staticmethod
    def is_it_sliding_piece_move(piece: int, direction: int) -> bool:
        """
        Static method used to check if this move should be calculated
        :param piece: int value of piece_square
        :param direction: int value of direction
        :return: bool value of if move should be calculated or not
        """
        if piece is None or direction is None:
            raise NullArgumentException("ARGUMENTS CANNOT BE NULLS!")
        if not SlidingPiecesUtil.is_it_sliding_piece(piece) or direction not in MoveEnum.SLIDING_DIRECTIONS.value:
            raise IllegalArgumentException("WRONG ARGUMENTS GIVEN TO METHOD!")
        diagonal_pieces: tuple[int, int] = (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value)
        diagonal_directions: tuple[int, int, int, int] = (MoveEnum.TOP_LEFT.value, MoveEnum.TOP_RIGHT.value,
                                                          MoveEnum.BOTTOM_LEFT.value, MoveEnum.BOTTOM_RIGHT.value)

        line_pieces: tuple[int, int] = (PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)
        line_directions: tuple[int, int, int, int] = (MoveEnum.TOP.value, MoveEnum.LEFT.value,
                                                      MoveEnum.RIGHT.value, MoveEnum.BOTTOM.value)

        if piece in diagonal_pieces and direction in diagonal_directions:
            return True
        return piece in line_pieces and direction in line_directions

    @staticmethod
    def is_it_sliding_piece(piece: int) -> bool:
        """
        Static method used to check if piece_square is a sliding piece_square.
        :param piece: int value of piece_square
        :return: bool value of if piece_square is sliding piece_square or not
        """
        if piece is None:
            raise NullArgumentException("PIECE CANNOT BE NULL!")
        return piece in (PiecesEnum.BISHOP.value, PiecesEnum.QUEEN.value, PiecesEnum.ROOK.value)
