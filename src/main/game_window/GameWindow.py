from numpy import array
from playsound import playsound
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from game_window.Canvas import Canvas
from game_window.ColorManager import ColorManager
from game_window.engine.Engine import Engine
from game_window.enums.CanvasEnum import CanvasEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.GameWindowUi import GameWindowUi
from game_window.Move import Move
from game_window.MoveGenerator import MoveGenerator
from game_window.MoveUtil import MoveUtil
from game_window.MoveValidator import MoveValidator
from game_window.PromotionData import PromotionData


class GameWindow(QWidget): # TODO Fen does not update counter when computer moves
    """
    Covers play game window.
    """
    __slots__ = array(["__ui", "__canvas", "__moving_piece", "__current_move", "__promotion_util"], dtype=str)

    def __init__(self):
        super(GameWindow, self).__init__()

        self.__canvas: Canvas = Canvas()
        self.__moving_piece: int = -1
        self.__current_move: Move = Move(None, None, None, -1)
        self.__promotion_util: PromotionData = PromotionData()

        with open("src/resources/styles/GameWindow.min.css", "r", encoding="utf-8") as style:
            self.__ui: GameWindowUi = GameWindowUi(self)
            self.setStyleSheet(style.read())
            self.__ui.get_new_game_button().clicked.connect(self.reset_game)
            self.__ui.get_switch_side_button().clicked.connect(self.switch_sides)

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Override paintEvent method to paint on canvas.
        :param event:
        :return: None
        """
        self.__canvas.begin(self)
        self.__canvas.draw_chess_board(self.__current_move)

        if self.__promotion_util.is_this_pawn_promoting():
            self.__canvas.paint_promotion_window(self.__promotion_util, self.__current_move.get_end_square())
        self.__canvas.end()

    def get_ui(self) -> GameWindowUi:
        """
        Gives access to PyQt5 Ui.
        :return: GameWindowUi instance
        """
        return self.__ui

    def __start_mouse_events(self, mouse_event: QMouseEvent) -> tuple[int, int] or tuple[None, None]:
        """
        Prepares row and col indexes for mouse press and release events
        :param mouse_event: QMouseEvent
        :return: row and col indexes if everything is good or None, None
        """
        if mouse_event.button() != Qt.LeftButton:
            return None, None

        canvas_width: int = CanvasEnum.CANVAS_WIDTH.value
        canvas_height: int = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x: int = mouse_event.x() - CanvasEnum.CANVAS_X.value
        current_position_y: int = mouse_event.y() - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 or current_position_y > canvas_height:
            return None, None

        col: int = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row: int = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        return row, col

    def mousePressEvent(self, mouse_press_event: QMouseEvent) -> None:
        """
        Override method which is used while user pressed mouse on QWidget.
        :param mouse_press_event: event of mouse pressed on QWidget
        :return: 
        """
        if not self.__canvas.get_board().get_legal_moves():
            return

        if self.__promotion_util.is_this_pawn_promoting():
            return
        row, col = self.__start_mouse_events(mouse_press_event)

        if row is None or col is None or not self.__canvas.get_board().should_this_piece_move(row, col):
            self.__current_move.set_start_square(None, None)
            self.__current_move.set_end_square(None, None)
            return

        self.__moving_piece: int = self.__canvas.get_board().delete_piece_from_board(row, col)
        piece_value: int = self.__moving_piece - ColorManager.get_piece_color(self.__moving_piece)

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
        if self.__promotion_util.is_this_pawn_promoting():
            self.__promotion_util.check_user_choice(mouse_release_event, self.__canvas.get_rect_height(),
                                                    self.__canvas.get_board())
            self.update_board_data()
            return
        row, col = self.__start_mouse_events(mouse_release_event)

        if self.__current_move.get_start_square() is None or row is None or col is None:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            return
        self.__current_move.set_end_square(row, col)

        if not self.__canvas.get_board().is_it_legal_move(
                self.__current_move) or self.__current_move.get_start_square() == self.__current_move.get_end_square():
            self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece,
                                                             self.__current_move.get_start_square())
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.__canvas.copy_current_move(self.__current_move)
            self.__current_move.set_start_square(None, None)
            self.__current_move.set_end_square(None, None)
            self.update()
            return
        self.__canvas.get_board().get_fen_data().update_move_counter()
        deleted_piece: int = self.__canvas.get_board().delete_piece_from_board(row, col)
        final_piece_index: int = 8 * row + col
        color: int = ColorManager.get_piece_color(self.__moving_piece)

        self.handle_castling_event(final_piece_index, color)
        deleted_piece: int = self.handle_pawn_special_events(mouse_release_event, color, final_piece_index,
                                                             deleted_piece)

        self.play_proper_sound(deleted_piece)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.__canvas.get_board().set_opposite_move_color()

        MoveUtil.update_no_sack_and_pawn_counter(self.__canvas.get_board().get_fen_data(), deleted_piece,
                                                 self.__current_move.get_moving_piece())
        self.update_board_data()

    def update_board_data(self) -> None:
        """
        Method used to update board data
        :return: None
        """
        self.__canvas.get_board().update_fen()

        print(self.__canvas.get_board().get_fen_string())
        if self.__promotion_util.is_this_pawn_promoting():
            return
        computer_move: Move = Engine.get_computer_move(self.__canvas.get_board())

        if computer_move is None:
            QMessageBox.about(self, "GAME IS OVER!", "CHECK MATE!")
            return

        deleted_piece: int = MoveUtil.update_board_with_engine_move(self.__canvas.get_board(), computer_move)
        self.play_proper_sound(deleted_piece)
        player_moves: list[Move] = MoveGenerator.generate_legal_moves(self.__canvas.get_board().get_player_color(),
                                                                      self.__canvas.get_board())
        self.__canvas.get_board().set_legal_moves(player_moves)
        self.__canvas.get_board().update_fen()
        print(self.__canvas.get_board().get_fen_string())
        self.__current_move = computer_move
        self.update()

    def handle_pawn_special_events(self, mouse_event: QMouseEvent, color: int, piece_index: int,
                                   deleted_piece: int) -> int:
        """
        Method used to handle every pawn special events
        :param mouse_event: mouse release event
        :param color: int value of color
        :param piece_index: int value of piece index
        :param deleted_piece: value of deleted piece
        :return: int
        """
        move_length: int = self.__current_move.get_end_square() - self.__current_move.get_start_square()

        if MoveValidator.is_pawn_promoting(self.__current_move, color, self.__canvas.get_board().get_engine_color()):
            self.__promotion_util.set_promotion_data(color, mouse_event.x(), mouse_event.y(),
                                                     piece_index)
        if MoveValidator.was_it_en_passant_move(self.__current_move, self.__canvas.get_board()):
            self.__canvas.get_board().make_en_passant_capture(self.__moving_piece)
            deleted_piece = 1
        elif move_length == MoveEnum.PAWN_UP_DOUBLE_MOVE.value and self.__current_move.get_moving_piece() == PiecesEnum.PAWN.value:
            self.__canvas.get_board().get_fen_data().set_en_passant_square(self.__current_move.get_end_square() -
                                                                           MoveEnum.PAWN_UP_SINGLE_MOVE.value)
            self.__canvas.get_board().get_fen_data().set_en_passant_piece_square(self.__current_move.get_end_square())
        elif move_length == MoveEnum.PAWN_DOWN_DOUBLE_MOVE.value and self.__current_move.get_moving_piece() == PiecesEnum.PAWN.value:
            self.__canvas.get_board().get_fen_data().set_en_passant_square(self.__current_move.get_end_square() -
                                                                           MoveEnum.PAWN_DOWN_SINGLE_MOVE.value)
            self.__canvas.get_board().get_fen_data().set_en_passant_piece_square(self.__current_move.get_end_square())
        elif self.__canvas.get_board().get_fen_data().get_en_passant_square() != -1:
            self.__canvas.get_board().get_fen_data().set_en_passant_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
            self.__canvas.get_board().get_fen_data().set_en_passant_piece_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
        return deleted_piece

    def handle_castling_event(self, final_piece_index: int, color: int) -> None:
        """
        Method used to handle castling movements
        :param final_piece_index: int value of piece index
        :param color: int value of color
        :return: None
        """
        if self.__current_move.get_moving_piece() == PiecesEnum.ROOK.value:
            MoveValidator.disable_castling_on_side(color, self.__current_move, self.__canvas.get_board())
        if MoveValidator.is_it_castling(self.__current_move):
            self.__canvas.get_board().castle_king(self.__moving_piece, self.__current_move)
        elif self.__current_move.get_moving_piece() == PiecesEnum.KING.value:
            self.__canvas.get_board().get_fen_data().set_castling_king_side(False, color)
            self.__canvas.get_board().get_fen_data().set_castling_queen_side(False, color)
            self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece, final_piece_index)
        else:
            self.__canvas.get_board().add_piece_to_the_board(self.__moving_piece, final_piece_index)

    def play_proper_sound(self, deleted_piece: int) -> None:
        """
        Plays proper sound effect based on deleted piece_square value
        :param deleted_piece: int value of piece_square
        :return: None
        """
        playsound("src/resources/sounds/Move.mp3") if deleted_piece == 0 else playsound(
            "src/resources/sounds/Capture.mp3")

    def reset_game(self) -> None:
        """
        Method used to reset the game state to the standard one
        :return: None
        """
        self.__canvas.get_board().__init__()
        self.__current_move.set_start_square(None, None)
        self.__current_move.set_end_square(None, None)
        self.update()

    def switch_sides(self) -> None:
        """
        Method used to switch sides of player and engine (colors)
        :return: None
        """
        self.__canvas.get_board().switch_colors()
        self.update()
