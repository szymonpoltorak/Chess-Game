from typing import Tuple

from numpy import array
from playsound import playsound
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenFactory import FenFactory
from game_window.board.fen.FenMaker import FenMaker
from game_window.Canvas import Canvas
from game_window.ColorManager import ColorManager
from game_window.engine.Engine import Engine
from game_window.engine.Evaluator import Evaluator
from game_window.enums.CanvasEnum import CanvasEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.Paths import Paths
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.enums.SpecialFlags import SpecialFlags
from game_window.GameWindowUi import GameWindowUi
from game_window.moving.EngineMover import EngineMover
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.pawns.PawnUtil import PawnUtil
from game_window.moving.Move import Move
from game_window.moving.MoveMakingUtil import MoveMakingUtil
from game_window.PromotionData import PromotionData


class GameWindow(QWidget):
    """
    Covers play game window.
    """
    __slots__ = array(["__ui", "__canvas", "__moving_piece", "__current_move", "__promotion_util", "__board"],
                      dtype=str)

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self) -> None:
        super(GameWindow, self).__init__()

        fen_factory: FenFactory = FenMaker(FenData(PiecesEnum.WHITE.value))

        self.__board = Board(fen_factory)
        self.__canvas: Canvas = Canvas()
        self.__moving_piece: int = -1
        self.__current_move: Move = Move(MoveEnum.NONE.value, MoveEnum.NONE.value, MoveEnum.NONE.value,
                                         MoveEnum.NONE.value)
        self.__promotion_util: PromotionData = PromotionData()

        with open(Paths.GAME_WINDOW_CSS.value, "r", encoding="utf-8") as style:
            self.__ui: GameWindowUi = GameWindowUi(self)
            self.setStyleSheet(style.read())
            self.__ui.get_new_game_button().clicked.connect(self.reset_game)
            self.__ui.get_switch_side_button().clicked.connect(self.switch_sides)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Method used to debug
        :param event:
        :return: None
        """
        super(GameWindow, self).keyPressEvent(event)
        self.keyPressed.emit(event)
        Evaluator.debug_evaluate_position(self.__board, 8)
        Evaluator.debug_evaluate_position(self.__board, 16)

    def paintEvent(self, event: QPaintEvent) -> None:
        """
        Override paintEvent method to paint on canvas.
        :param event:
        :return: None
        """
        self.__canvas.begin(self)
        self.__canvas.draw_chess_board(self.__current_move, self.__board)

        if self.__promotion_util.is_this_pawn_promoting():
            self.__canvas.paint_promotion_window(self.__promotion_util, self.__current_move.get_end_square())
        self.__canvas.end()

    def get_ui(self) -> GameWindowUi:
        """
        Gives access to PyQt5 Ui.
        :return: GameWindowUi instance
        """
        return self.__ui

    def __start_mouse_events(self, mouse_event: QMouseEvent) -> Tuple[int, int]:
        """
        Prepares row and col indexes for mouse press and release events
        :param mouse_event: QMouseEvent
        :return: row and col indexes if everything is good or None, None
        """
        if mouse_event.button() != Qt.LeftButton:
            return MoveEnum.NONE.value, MoveEnum.NONE.value

        canvas_width: int = CanvasEnum.CANVAS_WIDTH.value
        canvas_height: int = CanvasEnum.CANVAS_HEIGHT.value
        current_position_x: int = mouse_event.x() - CanvasEnum.CANVAS_X.value
        current_position_y: int = mouse_event.y() - CanvasEnum.CANVAS_Y.value

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 \
                or current_position_y > canvas_height:
            return MoveEnum.NONE.value, MoveEnum.NONE.value

        col: int = (current_position_x / self.__canvas.get_rect_width()).__floor__()
        row: int = (current_position_y / self.__canvas.get_rect_height()).__floor__()

        return row, col

    def mousePressEvent(self, mouse_press_event: QMouseEvent) -> None:
        """
        Override method which is used while user pressed mouse on QWidget.
        :param mouse_press_event: event of mouse pressed on QWidget
        :return: None
        """
        row, col = self.__start_mouse_events(mouse_press_event)

        if not self.__board.legal_moves() or self.__promotion_util.is_this_pawn_promoting():
            return

        if MoveEnum.NONE.value in (row, col) or not self.__board.should_this_piece_move(row, col):
            self.__current_move.set_start_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
            self.__current_move.set_end_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
            return

        self.__moving_piece = self.__board.delete_piece_from_board_square(8 * row + col)
        piece_value: int = self.__moving_piece - ColorManager.get_piece_color(self.__moving_piece)

        self.__current_move.set_start_square(row, col)
        self.__current_move.set_moving_piece(piece_value)

        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Override method which is triggered when mouse button is released.
        :param event: event of mouse released on QWidget
        :return: None
        """
        row, col = self.__start_mouse_events(event)
        start_square: int = self.__current_move.get_start_square()
        end_square: int = self.__current_move.get_end_square()

        if not self.check_quit_release_event_functions(start_square, row, col, end_square, event.x(), event.y()):
            return
        end_square = self.__current_move.get_end_square()
        self.__board.update_move_counter()

        final_piece_index: int = 8 * row + col
        deleted_piece: int = self.__board.delete_piece_from_board_square(final_piece_index)
        color: int = ColorManager.get_piece_color(self.__moving_piece)

        self.__board.disable_castling_if_captured_rook(deleted_piece, color, end_square)

        self.handle_castling_event(final_piece_index, color)

        deleted_piece = self.handle_pawn_special_events(color, final_piece_index, deleted_piece, event.x(), event.y())

        self.play_proper_sound(deleted_piece)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.__board.set_opposite_move_color()

        self.__board.update_no_sack_and_pawn_counter(deleted_piece, self.__current_move.get_moving_piece())
        self.update_board_data()

    def update_board_data(self) -> None:
        """
        Method used to update board data
        :return: None
        """
        self.__board.update_fen()

        if self.__promotion_util.is_this_pawn_promoting():
            return
        computer_move: Move = Engine.get_computer_move(self.__board)

        if computer_move is None:
            QMessageBox.about(self, "GAME IS OVER!", "CHECK MATE!")
            return
        deleted_piece: int = EngineMover.update_board_with_engine_move(self.__board, computer_move)
        self.__board.update_fen()

        self.play_proper_sound(deleted_piece)
        self.__board.update_legal_moves(self.__board.player_color())

        self.__current_move = computer_move
        self.update()

    def handle_pawn_special_events(self, color: int, piece_index: int, deleted_piece: int, mouse_x: int,
                                   mouse_y: int) -> int:
        """
        Method used to handle every pawn special events
        :param mouse_y: mouse x position int
        :param mouse_x: mouse y position y
        :param color: int value of color
        :param piece_index: int value of piece index
        :param deleted_piece: value of deleted piece
        :return: int
        """
        if PawnUtil.is_pawn_promoting(self.__current_move, color, self.__board.engine_color()):
            self.__promotion_util.set_promotion_data(color, mouse_x, mouse_y, piece_index)

        if PawnUtil.was_it_en_passant_move(self.__current_move, self.__board):
            MoveMakingUtil.make_en_passant_capture(self.__moving_piece, self.__board)
            deleted_piece = 1
        self.__board.update_fen_data_with_double_pawn_movement(self.__current_move)

        return deleted_piece

    def handle_castling_event(self, final_piece_index: int, color: int) -> None:
        """
        Method used to handle castling movements
        :param final_piece_index: int value of piece index
        :param color: int value of color
        :return: None
        """
        piece: int = self.__current_move.get_moving_piece()

        if piece == PiecesEnum.ROOK.value:
            self.__board.disable_castling_on_side(color, self.__current_move.get_start_square())

        if KingUtil.is_it_castling(self.__current_move):
            self.__current_move.set_special_flag(SpecialFlags.CASTLING.value)
            MoveMakingUtil.castle_king(self.__moving_piece, self.__current_move, self.__board)

        elif piece == PiecesEnum.KING.value:
            self.__board.set_castling_king_side(False, color)
            self.__board.set_castling_queen_side(False, color)
            self.__board.add_piece_to_the_board(self.__moving_piece, final_piece_index)
        else:
            self.__board.add_piece_to_the_board(self.__moving_piece, final_piece_index)

    def check_quit_release_event_functions(self, start_square: int, row: int, col: int, end_square: int, x: int,
                                           y: int) -> bool:
        """
        Method used to check conditions to end mouse event.
        """
        if self.__promotion_util.is_this_pawn_promoting():
            self.__promotion_util.check_user_choice(self.__canvas.get_rect_height(), self.__board, x, y)
            self.update_board_data()
            return False

        if start_square is None or MoveEnum.NONE.value in (row, col):
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            return False
        self.__current_move.set_end_square(row, col)

        if start_square == MoveEnum.NONE.value:
            return False

        if not self.__board.is_it_legal_move(self.__current_move) or start_square == end_square:
            self.__board.add_piece_to_the_board(self.__moving_piece, start_square)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.__canvas.copy_current_move(self.__current_move)
            self.__current_move.set_start_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
            self.__current_move.set_end_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
            self.update()
            return False
        return True

    def play_proper_sound(self, deleted_piece: int) -> None:
        """
        Plays proper sound effect based on deleted piece_square value
        :param deleted_piece: int value of piece_square
        :return: None
        """
        playsound(Paths.MOVE_SOUND.value) if deleted_piece == 0 else playsound(Paths.CAPTURE_SOUND.value)

    def reset_game(self) -> None:
        """
        Method used to reset the game state to the standard one
        :return: None
        """
        self.__board.__init__(FenMaker(FenData(PiecesEnum.WHITE.value)))
        self.__current_move.set_start_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
        self.__current_move.set_end_square(MoveEnum.NONE.value, MoveEnum.NONE.value)
        self.update()

    def switch_sides(self) -> None:
        """
        Method used to switch sides of player and engine (colors)
        :return: None
        """
        self.__board.switch_colors()
        self.update()
