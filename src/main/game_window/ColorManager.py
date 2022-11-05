from exceptions.IllegalArgumentException import IllegalArgumentException
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class ColorManager:
    """
    Class containing static methods to manage colors
    """

    __slots__ = ()

    @staticmethod
    def get_piece_color(piece: int) -> int:
        """
        Static method used to calculate the current piece_square color
        :param piece: int value of piece_square with color
        :return: int value of color
        """
        if piece == PiecesEnum.NONE.value:
            return PiecesEnum.NONE.value
        return PiecesEnum.WHITE.value if piece - PiecesEnum.BLACK.value < 0 else PiecesEnum.BLACK.value

    @staticmethod
    def get_opposite_piece_color(color: int) -> int:
        """
        Static method used to get opposite color value of given
        :param color: int value of color
        :return: int value of opposite color
        """
        if color == PiecesEnum.NONE.value:
            raise IllegalArgumentException("IT IS IMPOSSIBLE TO GET OPPOSITE COLOR OF NONE!")
        return PiecesEnum.WHITE.value if color == PiecesEnum.BLACK.value else PiecesEnum.BLACK.value

    @staticmethod
    def pick_proper_color(row: int, col: int) -> str:
        """
        Static method chooses proper color for end_square on a chess board based on row and col index.
        :param row: current row on chess board
        :param col: current column on chess board
        :return: string value of a color
        """
        is_light_color = (row + col) % 2 == 0
        return BoardEnum.PRIMARY_BOARD_COLOR.value if is_light_color else BoardEnum.SECONDARY_BOARD_COLOR.value

    @staticmethod
    def get_opposite_square_color(color: str) -> str:
        """
        Returns opposite color of given one.
        :param color: given color string of which we want to have opposite one
        :return: opposite color string
        """
        return BoardEnum.SECONDARY_BOARD_COLOR.value if color == BoardEnum.PRIMARY_BOARD_COLOR.value else \
            BoardEnum.PRIMARY_BOARD_COLOR.value

    @staticmethod
    def is_it_valid_color(color: int) -> bool:
        """
        Methods returns if piece color is a valid one
        :param color: int value of color
        :return: bool
        """
        return color in (PiecesEnum.BLACK.value, PiecesEnum.WHITE.value)
