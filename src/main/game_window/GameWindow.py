from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget
from numpy import array

from game_window.Canvas import Canvas
from game_window.GameWindowUi import GameWindowUi
from game_window.enums.CanvasEnum import CanvasEnum


class GameWindow(QWidget):
    """
    Covers play game window.
    """
    __slots__ = array(["__ui", "__canvas", "__canvas_monitor"])

    def __init__(self):
        super(GameWindow, self).__init__()

        self.__canvas = Canvas()

        with open("src/resources/styles/GameWindow.min.css", "r", encoding="utf-8") as style:
            self.__ui = GameWindowUi(self)
            self.setStyleSheet(style.read())

    def paintEvent(self, event) -> None:
        """
        Override paintEvent method to paint on canvas.
        :param event:
        :return: None
        """
        self.__canvas.begin(self)
        self.__canvas.draw_chess_board()
        self.__canvas.end()

    def get_ui(self) -> GameWindowUi:
        """
        Gives access to PyQt5 Ui.
        :return: GameWindowUi instance
        """
        return self.__ui

    def mousePressEvent(self, mouse_event) -> None:
        mouse_x = mouse_event.x()
        mouse_y = mouse_event.y()
        canvas_width = CanvasEnum.CANVAS_WIDTH.value
        canvas_height = CanvasEnum.CANVAS_HEIGHT.value
        canvas_x = CanvasEnum.CANVAS_X.value
        canvas_y = CanvasEnum.CANVAS_Y.value
        current_position_x = mouse_x - CanvasEnum.CANVAS_X.value
        current_position_y = mouse_y - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return
        print(f"X: {mouse_event.x()} Y: {mouse_event.y()}")
        print(f"Current X: {current_position_x} Current Y: {current_position_y}")

        rect_index_x = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        rect_index_y = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        print(f"Rect X: {rect_index_x} Rect Y: {rect_index_y}")


    def update_board_display(self) -> None:
        self.__canvas.draw_chess_board()
        self.update()
