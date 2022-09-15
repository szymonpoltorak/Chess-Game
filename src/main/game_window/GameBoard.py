import pygame

from game_window.BoardEnum import BoardEnum


class GameBoard:
    __slots__ = ("__surface", "__rect_width", "__rect_height", "__canvas")

    def __init__(self, surface):
        self.__surface = surface
        self.__rect_width = int(surface.get_width() / 8)
        self.__rect_height = int(surface.get_height() / 8)

    def draw_chess_board(self):
        present_x = 0
        present_y = 0
        number = 8
        index_x = 0
        index_y = 0
        letters = ("a", "b", "c", "d", "e", "f", "g", "h")
        letter_index = 0

        for row in range(BoardEnum.BOARD_SIZE.value):
            for col in range(BoardEnum.BOARD_SIZE.value):
                color = self.pick_proper_color(row, col)
                rectangle = pygame.Rect(present_x, present_y, self.__rect_width, self.__rect_height)

                pygame.draw.rect(self.__surface, color, rectangle)
                present_x += self.__rect_width

                if self.should_i_draw_number(col):
                    self.draw_character_on_board(number, index_x + 10, index_y + 10, self.get_opposite_color(color))
                    number -= 1
                if self.should_i_draw_letter(row):
                    self.draw_character_on_board(letters[letter_index], index_x + 67, index_y + 67,
                                                 self.get_opposite_color(color))
                    letter_index += 1
                    index_x = present_x

            present_y += self.__rect_height
            present_x = 0
            index_y = present_y

    def pick_proper_color(self, row: int, col: int):
        is_light_color = (row + col) % 2 == 0

        if is_light_color:
            return BoardEnum.PRIMARY_BOARD_COLOR.value
        else:
            return BoardEnum.SECONDARY_BOARD_COLOR.value

    def should_i_draw_number(self, col: int):
        return col == 0

    def should_i_draw_letter(self, row: int):
        return row == 7

    def get_opposite_color(self, color: str):
        if color == BoardEnum.PRIMARY_BOARD_COLOR.value:
            return BoardEnum.SECONDARY_BOARD_COLOR.value
        else:
            return BoardEnum.PRIMARY_BOARD_COLOR.value

    def draw_character_on_board(self, character, position_x: int, position_y: int, color: str):
        font = pygame.font.SysFont("Monospace Bold", BoardEnum.CHARACTER_SIZE.value)
        text = font.render(str(character), True, color)
        self.__surface.blit(text, (position_x, position_y))

    def get_surface(self):
        return self.__surface
