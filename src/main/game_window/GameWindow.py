from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget
from pygame.surface import Surface

from game_window.BoardPainter import BoardPainter
from game_window.enums.PyGameEnum import PyGameEnum
from game_window.GameWindowUi import GameWindowUi


class GameWindow(QWidget):
    """
    Integrates PyQt5 Gui with PyGame Chess Board in one window and manages it.
    """
    __slots__ = ("__ui", "__data", "__image", "__board_painter")

    def __init__(self, canvas: Surface):
        super(GameWindow, self).__init__()

        self.__data = None
        self.__image = None
        self.__board_painter = BoardPainter(canvas)

        with open("src/resources/styles/GameWindow.min.css", "r", encoding="utf-8") as style:
            self.__ui = GameWindowUi(self)
            self.setStyleSheet(style.read())

        self.update_board_display()

    def paintEvent(self, event):
        """
        Override paintEvent method to paint on pygame canvas.
        :param event:
        :return: void
        """
        canvas_painter = QtGui.QPainter()
        canvas_painter.begin(self)
        canvas_painter.drawImage(PyGameEnum.CANVAS_X.value, PyGameEnum.CANVAS_Y.value, self.__image)
        canvas_painter.end()

    def get_ui(self):
        """
        Gives access to PyQt5 Ui.
        :return: GameWindowUi instance
        """
        return self.__ui

    def update_board_display(self):
        self.__board_painter.draw_chess_board()

        canvas = self.__board_painter.get_canvas()
        width = canvas.get_width()
        height = canvas.get_height()

        self.__data = canvas.get_buffer().raw
        self.__image = QtGui.QImage(self.__data, width, height, QtGui.QImage.Format_RGB32)
        self.update()
