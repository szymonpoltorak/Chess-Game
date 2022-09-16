import pygame
from pygame.surface import Surface

from game_window.Board import Board
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.PiecesEnum import PiecesEnum


class BoardPainter:
    __slots__ = ("__canvas", "__rect_width", "__rect_height", "__board")

    def __init__(self, canvas):
        self.__canvas: Surface = canvas
        self.__rect_width: int = int(canvas.get_width() / 8)
        self.__rect_height: int = int(canvas.get_height() / 8)
        self.__board: Board = Board()

    def draw_chess_board(self):
        current_x = 0
        current_y = 0
        index_x = 0
        index_y = 0

        current_number = 8
        letters = ("a", "b", "c", "d", "e", "f", "g", "h")

        for row in range(BoardEnum.BOARD_SIZE.value):
            for col in range(BoardEnum.BOARD_SIZE.value):
                color = self.pick_proper_color(row, col)
                rectangle = pygame.Rect(current_x, current_y, self.__rect_width, self.__rect_height)

                pygame.draw.rect(self.__canvas, color, rectangle)
                current_x += self.__rect_width

                if col == 0:
                    self.draw_character_on_board(current_number, index_x + BoardEnum.NUMBER_SCALE_X.value,
                                                 index_y + BoardEnum.NUMBER_SCALE_Y.value,
                                                 self.get_opposite_color(color))
                    current_number -= 1
                if row == 7:
                    self.draw_character_on_board(letters[col], index_x + BoardEnum.LETTER_SCALE_X.value,
                                                 index_y + BoardEnum.LETTER_SCALE_Y.value,
                                                 self.get_opposite_color(color))
                    index_x = current_x

            current_y += self.__rect_height
            current_x = 0
            index_y = current_y
        self.__draw_position_from_fen()

    def __draw_position_from_fen(self):
        fen = self.__board.get_fen_string().replace('/', ' ').split()
        current_x = 0
        current_y = 0

        for row in range(BoardEnum.BOARD_SIZE.value):
            row_pieces = [*fen[row]]

            for col in range(len(row_pieces)):
                self.load_proper_image(current_x, current_y, row_pieces[col])
                current_x += self.__rect_width
            current_x = 0
            current_y += self.__rect_height

    def load_proper_image(self, current_x: int, current_y: int, piece_letter: str):
        try:
            int(piece_letter)
            return
        except ValueError:
            color = None
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

    def pick_proper_color(self, row: int, col: int):
        is_light_color = (row + col) % 2 == 0

        if is_light_color:
            return BoardEnum.PRIMARY_BOARD_COLOR.value
        else:
            return BoardEnum.SECONDARY_BOARD_COLOR.value

    def get_opposite_color(self, color: str):
        if color == BoardEnum.PRIMARY_BOARD_COLOR.value:
            return BoardEnum.SECONDARY_BOARD_COLOR.value
        else:
            return BoardEnum.PRIMARY_BOARD_COLOR.value

    def draw_character_on_board(self, character, position_x: int, position_y: int, color: str):
        font = pygame.font.SysFont("Monospace Bold", BoardEnum.CHARACTER_SIZE.value)
        text = font.render(str(character), True, color)
        self.__canvas.blit(text, (position_x, position_y))

    def get_surface(self):
        return self.__canvas

    def get_board(self):
        return self.__board
