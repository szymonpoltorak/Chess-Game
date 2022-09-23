from numpy import array
from playsound import playsound
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget

from game_window.Canvas import Canvas
from game_window.ColorManager import ColorManager
from game_window.enums.CanvasEnum import CanvasEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.GameWindowUi import GameWindowUi
from game_window.Move import Move
from game_window.MoveGenerator import MoveGenerator
from game_window.MoveValidator import MoveValidator


class GameWindow(QWidget):
    """
    Covers play game window.
    """
    __slots__ = array(["__ui", "__canvas", "__moving_piece", "__current_move"])

    def __init__(self):
        super(GameWindow, self).__init__()

        self.__canvas = Canvas()
        self.__moving_piece = None
        self.__current_move = Move(None, None, None)

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
        self.__canvas.draw_chess_board(self.__current_move)
        self.__canvas.end()

    def get_ui(self) -> GameWindowUi:
        """
        Gives access to PyQt5 Ui.
        :return: GameWindowUi instance
        """
        return self.__ui

    def __start_mouse_events(self, mouse_event: QMouseEvent):
        """
        Prepares row and col indexes for mouse press and release events
        :param mouse_event: QMouseEvent
        :return: row and col indexes if everything is good or None, None
        """
        if mouse_event.button() != Qt.LeftButton:
            return None, None

        canvas_width = CanvasEnum.CANVAS_WIDTH.value
        canvas_height = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x = mouse_event.x() - CanvasEnum.CANVAS_X.value
        current_position_y = mouse_event.y() - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return None, None

        col = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        return row, col

    def mousePressEvent(self, mouse_press_event: QMouseEvent) -> None:
        """
        Override method which is used while user pressed mouse on QWidget.
        :param mouse_press_event: event of mouse pressed on QWidget
        :return: 
        """
        row, col = self.__start_mouse_events(mouse_press_event)

        if row is None or col is None or not self.__canvas.get_board().should_this_piece_move(row, col):
            self.__current_move.set_start_square(None, None)
            return

        self.__moving_piece = self.__canvas.get_board().delete_piece_from_board(row, col)
        piece_value = self.__moving_piece - ColorManager.get_piece_color(self.__moving_piece)

        self.__current_move.set_start_square(row, col)
        self.__current_move.set_moving_piece(piece_value)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.update()

    def mouseReleaseEvent(self, mouse_release_event: QMouseEvent) -> None:
        """
        Override method which is triggered when mouse button is released.
        :param mouse_release_event: event of mouse released on QWidget
        :return: None
        """
        row, col = self.__start_mouse_events(mouse_release_event)

        if self.__current_move.get_start_square() is None or row is None or col is None:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            return
        self.__current_move.set_end_square(row, col)

        if not self.__canvas.get_board().is_it_legal_move(self.__current_move) or self.__current_move.get_start_square() == self.__current_move.get_end_square():
            self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece, self.__current_move.get_start_square())
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.__canvas.copy_current_move(self.__current_move)
            self.__current_move.set_start_square(None, None)
            self.__current_move.set_end_square(None, None)
            self.update()
            return
        deleted_piece = self.__canvas.get_board().delete_piece_from_board(row, col)
        final_piece_index = 8 * row + col
        move_length = self.__current_move.get_end_square() - self.__current_move.get_start_square()

        if self.__current_move.get_moving_piece() == PiecesEnum.ROOK.value:
            color = ColorManager.get_piece_color(self.__moving_piece)
            MoveValidator.disable_castling_on_side(color, self.__current_move, self.__canvas.get_board())

        if MoveValidator.is_it_castling(self.__current_move):
            self.__canvas.get_board().castle_king(self.__moving_piece, self.__current_move)
        else:
            self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece, final_piece_index)

        if MoveValidator.was_it_en_passant_move(self.__current_move, self.__canvas.get_board()):
            self.__canvas.get_board().make_en_passant_capture(self.__moving_piece)
            deleted_piece = 1
        elif move_length == MoveEnum.PAWN_UP_DOUBLE_MOVE.value and self.__current_move.get_moving_piece() == PiecesEnum.PAWN.value:
            self.__canvas.get_board().set_en_passant_square(self.__current_move.get_end_square() -
                                                            MoveEnum.PAWN_UP_SINGLE_MOVE.value)
            self.__canvas.get_board().set_en_passant_piece_square(self.__current_move.get_end_square())
        elif move_length == MoveEnum.PAWN_DOWN_DOUBLE_MOVE.value and self.__current_move.get_moving_piece() == PiecesEnum.PAWN.value:
            self.__canvas.get_board().set_en_passant_square(self.__current_move.get_end_square() -
                                                            MoveEnum.PAWN_DOWN_SINGLE_MOVE.value)
            self.__canvas.get_board().set_en_passant_piece_square(self.__current_move.get_end_square())
        self.play_proper_sound(deleted_piece)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.__canvas.get_board().set_opposite_move_color()
        list_move = MoveGenerator.generate_legal_moves(ColorManager.get_opposite_piece_color(
                                        ColorManager.get_piece_color(self.__moving_piece)), self.__canvas.get_board())
        self.__canvas.get_board().set_legal_moves(list_move)
        self.update()

    def play_proper_sound(self, deleted_piece: int) -> None:
        """
        Plays proper sound effect based on deleted piece_square value
        :param deleted_piece: int value of piece_square
        :return: None
        """
        if deleted_piece == 0:
            playsound("src/resources/sounds/Move.mp3")
        else:
            playsound("src/resources/sounds/Capture.mp3")
