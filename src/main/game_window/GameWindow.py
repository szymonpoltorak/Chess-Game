from PyQt5.QtWidgets import QWidget
from numpy import array

from game_window.Canvas import Canvas
from game_window.GameWindowUi import GameWindowUi


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

    def update_board_display(self) -> None:
        self.__canvas.draw_chess_board()
        self.update()
