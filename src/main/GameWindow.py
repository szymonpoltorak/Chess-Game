import ctypes

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget

from src.main.GameWindowUi_test import GameWindowUi


class GameWindow(QWidget):
    __slots__ = ("__ui", "__data", "__image")

    def __init__(self, canvas):
        super(GameWindow, self).__init__()
        width = canvas.get_width()
        height = canvas.get_height()
        appid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

        with open("src/resources/styles/GameWindow.min.css", "r", encoding="utf-8") as style:
            self.__ui = GameWindowUi()
            self.__ui.setup_ui(self)
            self.__data = canvas.get_buffer().raw
            self.__image = QtGui.QImage(self.__data, width, height, QtGui.QImage.Format_RGB32)
            self.setStyleSheet(style.read())

    def paintEvent(self, event):
        canvas_painter = QtGui.QPainter()
        canvas_painter.begin(self)
        canvas_painter.drawImage(150, 80, self.__image)
        canvas_painter.end()

    def get_ui(self):
        return self.__ui
