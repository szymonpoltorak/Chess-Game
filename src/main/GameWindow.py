from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

from PyGameEnum import PyGameEnum
from src.main.GameWindowUi import GameWindowUi


class GameWindow(QWidget):
    """
    Integrates PyQt5 Gui with PyGame Chess Board in one window and manages it.
    """
    __slots__ = ("__ui", "__data", "__image")

    def __init__(self, canvas):
        super(GameWindow, self).__init__()
        width = canvas.get_width()
        height = canvas.get_height()

        with open("src/resources/styles/GameWindow.min.css", "r", encoding="utf-8") as style:
            self.__ui = GameWindowUi(self)
            self.__data = canvas.get_buffer().raw
            self.__image = QtGui.QImage(self.__data, width, height, QtGui.QImage.Format_RGB32)
            self.setStyleSheet(style.read())

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
