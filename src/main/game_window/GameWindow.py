from numpy import array
from playsound import playsound
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from game_window.Canvas import Canvas
from game_window.enums.CanvasEnum import CanvasEnum
from game_window.GameWindowUi import GameWindowUi


class GameWindow(QWidget):
    """
    Covers play game window.
    """
    __slots__ = array(["__ui", "__canvas", "__moving_piece"])

    def __init__(self):
        super(GameWindow, self).__init__()

        self.__canvas = Canvas()
        self.__moving_piece = None

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

    def mousePressEvent(self, mouse_press_event) -> None:
        """
        Override method which is used while user pressed mouse on QWidget.
        :param mouse_press_event: event of mouse pressed on QWidget
        :return: 
        """

        if mouse_press_event.button() != Qt.LeftButton:
            return

        canvas_width = CanvasEnum.CANVAS_WIDTH.value
        canvas_height = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x = mouse_press_event.x() - CanvasEnum.CANVAS_X.value
        current_position_y = mouse_press_event.y() - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return

        col = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        self.__moving_piece = self.__canvas.get_board().delete_piece_from_board(row, col)
        self.update()

    def mouseReleaseEvent(self, mouse_release_event) -> None:
        """
        Override method which is triggered when mouse button is released.
        :param mouse_release_event: event of mouse released on QWidget
        :return: None
        """

        if mouse_release_event.button() != Qt.LeftButton:
            return

        canvas_width = CanvasEnum.CANVAS_WIDTH.value
        canvas_height = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x = mouse_release_event.x() - CanvasEnum.CANVAS_X.value
        current_position_y = mouse_release_event.y() - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return

        col = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        deleted_piece = self.__canvas.get_board().delete_piece_from_board(row, col)
        self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece, row, col)

        if deleted_piece == 0:
            playsound("src/resources/sounds/Move.mp3")
        else:
            playsound("src/resources/sounds/Capture.mp3")
        self.update()

    def update_board_display(self) -> None:
        """
        Method used to update the chess board canvas.
        :return: None
        """
        self.__canvas.draw_chess_board()
        self.update()
