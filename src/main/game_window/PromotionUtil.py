from numpy import array
from PyQt5.QtGui import QMouseEvent

from game_window.enums.PiecesEnum import PiecesEnum


class PromotionUtil:
    __slots__ = array(["__piece_color", "__position_x", "__position_y", "__is_promoting", "__square"])

    def __init__(self):
        self.__piece_color = -1
        self.__position_x = -1
        self.__position_y = -1
        self.__is_promoting = False
        self.__square = -1

    def set_promotion_data(self, color: int, x: int, y: int, square: int):
        self.__piece_color = color
        self.__position_x = x
        self.__position_y = y
        self.__is_promoting = True
        self.__square = square

    def get_position_x(self):
        return self.__position_x

    def get_position_y(self):
        return self.__position_y

    def get_piece_color(self):
        return self.__piece_color

    def get_pawn_square(self):
        return self.__square

    def is_this_pawn_promoting(self):
        return self.__is_promoting

    def check_user_choice(self, mouse_event: QMouseEvent, rect_size: int, board):
        bond_x = self.__position_x + rect_size
        bond_y = self.__position_y + 4 * rect_size
        x = mouse_event.x()
        y = mouse_event.y()

        if x < self.__position_x or x > bond_x or y > bond_y or y < self.__position_y:
            return
        pieces = array([PiecesEnum.QUEEN.value, PiecesEnum.BISHOP.value, PiecesEnum.KNIGHT.value,
                        PiecesEnum.ROOK.value])
        print(f"Index : {self.get_rect_index(y, rect_size)}")
        board.get_board_array()[self.__square] = self.__piece_color | pieces[self.get_rect_index(y, rect_size)]
        board.convert_board_to_string()
        self.__is_promoting = False

    def get_rect_index(self, y: int, rect_size: int):
        low_bond = self.__position_y
        high_bond = self.__position_y + rect_size

        for index in range(4):
            if low_bond < y < high_bond:
                return index
            low_bond += rect_size
            high_bond += rect_size
        return -1

    def __str__(self):
        return f"Color : {self.__piece_color}\nX : {self.__position_x}\nY : {self.__position_y}\n" \
               f"IsPromoting : {self.__is_promoting}\nSquare : {self.__square}\n"
