from abc import ABC
from abc import abstractmethod

from game_window.board.Board import Board


class Promoter(ABC):
    """
    Abstract class for Promoting Pawns
    """

    __slots__ = ()

    @abstractmethod
    def set_promotion_data(self, color: int, x: int, y: int, square: int) -> None:
        """
        Method used to set promotion data fields
        :param color: int value of color
        :param x: int x position
        :param y: int y position
        :param square: int value of end_square
        :return: None
        """
        pass

    @abstractmethod
    def check_user_choice(self, rect_size: int, board: Board, x: int, y: int) -> None:
        """
        Method used to check user promotion choice
        :param x: mouse x coordinates int
        :param y: mouse y coordinates int
        :param rect_size: int value of rectangle size
        :param board: Board instance
        :return: None
        """
        pass

    @abstractmethod
    def get_piece_color(self) -> int:
        """
        Gives access to color value of piece
        :return: int
        """
        pass

    @abstractmethod
    def get_pawn_square(self) -> int:
        """
        Gives access to pawn end_square index
        :return: int
        """
        pass

    @abstractmethod
    def is_this_pawn_promoting(self) -> bool:
        """
        Tells if pawn is promoting or not
        :return: bool
        """
        pass
