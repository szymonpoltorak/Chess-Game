from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class ColorManager:
    @staticmethod
    def get_piece_color(piece: int) -> int:
        if piece == PiecesEnum.NONE.value:
            return PiecesEnum.NONE.value
        elif piece - PiecesEnum.BLACK.value < 0:
            return PiecesEnum.WHITE.value
        return PiecesEnum.BLACK.value

    @staticmethod
    def get_opposite_piece_color(color: int) -> int:
        if color == PiecesEnum.BLACK.value:
            return PiecesEnum.WHITE.value
        return PiecesEnum.BLACK.value

    @staticmethod
    def pick_proper_color(row: int, col: int) -> str:
        """
        Method chooses proper color for square on a chess board based on row and col index.
        :param row: current row on chess board
        :param col: current column on chess board
        :return: string value of a color
        """
        is_light_color = (row + col) % 2 == 0

        if is_light_color:
            return BoardEnum.PRIMARY_BOARD_COLOR.value
        else:
            return BoardEnum.SECONDARY_BOARD_COLOR.value

    @staticmethod
    def get_opposite_square_color(color: str) -> str:
        """
        Returns opposite color of given one.
        :param color: given color string of which we want to have opposite one
        :return: opposite color string
        """
        if color == BoardEnum.PRIMARY_BOARD_COLOR.value:
            return BoardEnum.SECONDARY_BOARD_COLOR.value
        else:
            return BoardEnum.PRIMARY_BOARD_COLOR.value
