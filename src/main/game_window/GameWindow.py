from numpy import array
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

    def mousePressEvent(self, mouse_event) -> None:
        mouse_x = mouse_event.x()
        mouse_y = mouse_event.y()
        canvas_width = CanvasEnum.CANVAS_WIDTH.value
        canvas_height = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x = mouse_x - CanvasEnum.CANVAS_X.value
        current_position_y = mouse_y - CanvasEnum.CANVAS_Y.value
        board = self.__canvas.get_board()

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return

        col = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        self.__moving_piece = board.delete_piece_from_board(row, col)
        self.update()

    def mouseReleaseEvent(self, mouse_event) -> None:
        mouse_x = mouse_event.x()
        mouse_y = mouse_event.y()

        canvas_width = CanvasEnum.CANVAS_WIDTH.value
        canvas_height = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x = mouse_x - CanvasEnum.CANVAS_X.value
        current_position_y = mouse_y - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return

        col = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        self.__canvas.get_board().delete_piece_from_board(row, col)
        self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece, row, col)
        self.update()

    def update_board_display(self) -> None:
        self.__canvas.draw_chess_board()
        self.update()
