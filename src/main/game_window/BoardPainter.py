import pygame
from pygame.surface import Surface

from game_window.Board import Board
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class BoardPainter:
    __slots__ = ("__canvas", "__rect_width", "__rect_height", "__board")

    def __init__(self, canvas: Surface):
        self.__canvas: Surface = canvas
        self.__rect_width: int = int(canvas.get_width() / 8)
        self.__rect_height: int = int(canvas.get_height() / 8)
        self.__board: Board = Board()

    def draw_chess_board(self) -> None:
        """
        Method draws a whole chess board on canvas.
        :return: None
        """
        current_x = 0
        current_y = 0
        index_x = 0
        index_y = 0

        current_number = 8
        letters = ("a", "b", "c", "d", "e", "f", "g", "h")

        for row in range(BoardEnum.BOARD_LENGTH.value):
            for col in range(BoardEnum.BOARD_LENGTH.value):
                color = self.pick_proper_color(row, col)
                rectangle = pygame.Rect(current_x, current_y, self.__rect_width, self.__rect_height)

                pygame.draw.rect(self.__canvas, color, rectangle)
                current_x += self.__rect_width

                if col == 0:
                    self._draw_character_on_board(current_number, index_x + BoardEnum.NUMBER_SCALE_X.value,
                                                  index_y + BoardEnum.NUMBER_SCALE_Y.value,
                                                  self.get_opposite_color(color))
                    current_number -= 1
                if row == 7:
                    self._draw_character_on_board(letters[col], index_x + BoardEnum.LETTER_SCALE_X.value,
                                                  index_y + BoardEnum.LETTER_SCALE_Y.value,
                                                  self.get_opposite_color(color))
                    index_x = current_x

            current_y += self.__rect_height
            current_x = 0
            index_y = current_y
        self.__draw_position_from_fen()

    def __draw_position_from_fen(self) -> None:
        """
        Method draws pieces on chess board from fen string representation.
        :return: None
        """
        fen = self.__board.get_fen_string().replace('/', ' ').split()
        current_x = 0
        current_y = 0

        for row in range(BoardEnum.BOARD_LENGTH.value):
            row_pieces = [*fen[row]]

            for col in range(len(row_pieces)):
                current_x = self.load_proper_image(current_x, current_y, row_pieces[col])
            current_x = 0
            current_y += self.__rect_height

    def load_proper_image(self, current_x: int, current_y: int, piece_letter: str) -> int:
        """
        Loads image from resources based on current letter loaded from fen string.
        :param current_x: current x coordinate from which we start drawing.
        :param current_y: current y coordinate from which we start drawing.
        :param piece_letter: letter representing piece on chess board, got from fen string.
        :return: x coordinate of current square
        """
        try:
            blank_spaces = int(piece_letter)
            current_x += blank_spaces * self.__rect_width

            return current_x
        except ValueError:
            piece = piece_letter.upper()
            image_path = "src/resources/images/pieces/"
            extension = ".png"

            if piece_letter.isupper():
                color = "w"
            else:
                color = "b"

            image = pygame.image.load(image_path + color + piece + extension)
            image = pygame.transform.smoothscale(image, (PiecesEnum.SCALE_WIDTH.value, PiecesEnum.SCALE_HEIGHT.value))
            self.__canvas.blit(image, (PiecesEnum.SCALE_X.value + current_x, PiecesEnum.SCALE_Y.value + current_y))

            current_x += self.__rect_width

            return current_x

    def pick_proper_color(self, row: int, col: int) -> str:
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

    def get_opposite_color(self, color: str) -> str:
        """
        Returns opposite color of given one.
        :param color: given color string of which we want to have opposite one
        :return: opposite color string
        """
        if color == BoardEnum.PRIMARY_BOARD_COLOR.value:
            return BoardEnum.SECONDARY_BOARD_COLOR.value
        else:
            return BoardEnum.PRIMARY_BOARD_COLOR.value

    def _draw_character_on_board(self, character, position_x: int, position_y: int, color: str) -> None:
        """
        Draw characters : number and letters on board edges.
        :param character: characters string which we want to paint on canvas
        :param position_x: x coordinate where we want to start drawing character
        :param position_y: y coordinate where we want to start drawing character
        :param color: color string which we want a character to have
        :return: None
        """
        font = pygame.font.SysFont("Monospace Bold", BoardEnum.CHARACTER_SIZE.value)
        text = font.render(str(character), True, color)
        self.__canvas.blit(text, (position_x, position_y))

    def get_canvas(self) -> Surface:
        """
        Gives access to pygame canvas
        :return: canvas instance
        """
        return self.__canvas

    def get_board(self) -> Board:
        """
        Gives access to Board object instance.
        :return: board instance
        """
        return self.__board
