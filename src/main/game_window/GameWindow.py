from numpy import array
from playsound import playsound
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QWidget

from game_window.board.Board import Board
from game_window.board.fen.FenData import FenData
from game_window.board.fen.FenUtil import FenUtil
from game_window.Canvas import Canvas
from game_window.ColorManager import ColorManager
from game_window.engine.Engine import Engine
from game_window.engine.Evaluator import Evaluator
from game_window.enums.CanvasEnum import CanvasEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.GameWindowUi import GameWindowUi
from game_window.moving.EngineMover import EngineMover
from game_window.moving.generation.king_and_knights.KingUtil import KingUtil
from game_window.moving.generation.MoveGenerator import MoveGenerator
from game_window.moving.generation.pawns.PawnUtil import PawnUtil
from game_window.moving.Move import Move
from game_window.moving.MoveList import MoveList
from game_window.PromotionData import PromotionData


class GameWindow(QWidget):
    """
    Covers play game window.
    """
    __slots__ = array(["__ui", "__canvas", "__moving_piece", "__current_move", "__promotion_util", "__board"],
                      dtype=str)

    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self):
        super(GameWindow, self).__init__()

        self.__board = Board()
        self.__canvas: Canvas = Canvas()
        self.__moving_piece: int = -1
        self.__current_move: Move = Move(None, None, None, -1)
        self.__promotion_util: PromotionData = PromotionData()

        with open("src/resources/styles/GameWindow.min.css", "r", encoding="utf-8") as style:
            self.__ui: GameWindowUi = GameWindowUi(self)
            self.setStyleSheet(style.read())
            self.__ui.get_new_game_button().clicked.connect(self.reset_game)
            self.__ui.get_switch_side_button().clicked.connect(self.switch_sides)

    def keyPressEvent(self, event) -> None:
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

        if current_position_x < 0 or current_position_x > canvas_width or current_position_y < 0 \
                or current_position_y > canvas_height:
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
        row, col = self.__start_mouse_events(mouse_press_event)

        if not self.__board.get_legal_moves() or self.__promotion_util.is_this_pawn_promoting():
            return

        if row is None or col is None or not self.__board.should_this_piece_move(row, col):
            self.__current_move.set_start_square(None, None)
            self.__current_move.set_end_square(None, None)
            return

        self.__moving_piece: int = self.__board.delete_piece_from_board(row, col)
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
        fen_data: FenData = self.__board.get_fen_data()

        if not self.check_quit_release_event_functions(start_square, row, col, end_square, event):
            return

        fen_data.update_move_counter()
        deleted_piece: int = self.__board.delete_piece_from_board(row, col)
        final_piece_index: int = 8 * row + col
        color: int = ColorManager.get_piece_color(self.__moving_piece)

        FenUtil.disable_castling_if_deleted_rook(deleted_piece, color, end_square, self.__board)

        self.handle_castling_event(final_piece_index, color)
        deleted_piece: int = self.handle_pawn_special_events(event, color, final_piece_index, deleted_piece)

        self.play_proper_sound(deleted_piece)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.__board.set_opposite_move_color()

        FenUtil.update_no_sack_and_pawn_counter(fen_data, deleted_piece, self.__current_move.get_moving_piece())
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

        self.play_proper_sound(deleted_piece)
        player_moves: MoveList = MoveGenerator.generate_legal_moves(self.__board.get_color_to_move(), self.__board)
        self.__board.set_legal_moves(player_moves)
        self.__board.update_fen()

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
        end_square: int = self.__current_move.get_end_square()
        move_length: int = end_square - self.__current_move.get_start_square()
        fen_data: FenData = self.__board.get_fen_data()
        moving_piece: int = self.__current_move.get_moving_piece()

        if PawnUtil.is_pawn_promoting(self.__current_move, color, self.__board.get_engine_color()):
            self.__promotion_util.set_promotion_data(color, mouse_event.x(), mouse_event.y(), piece_index)

        if PawnUtil.was_it_en_passant_move(self.__current_move, self.__board):
            self.__board.make_en_passant_capture(self.__moving_piece)
            deleted_piece = 1

        elif move_length == MoveEnum.PAWN_UP_DOUBLE_MOVE.value and moving_piece == PiecesEnum.PAWN.value:
            fen_data.set_en_passant_square(end_square - MoveEnum.PAWN_UP_SINGLE_MOVE.value)
            fen_data.set_en_passant_piece_square(end_square)

        elif move_length == MoveEnum.PAWN_DOWN_DOUBLE_MOVE.value and moving_piece == PiecesEnum.PAWN.value:
            fen_data.set_en_passant_square(end_square - MoveEnum.PAWN_DOWN_SINGLE_MOVE.value)
            fen_data.set_en_passant_piece_square(end_square)

        elif fen_data.get_en_passant_square() != -1:
            fen_data.set_en_passant_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
            fen_data.set_en_passant_piece_square(MoveEnum.NONE_EN_PASSANT_SQUARE.value)
        return deleted_piece

    def handle_castling_event(self, final_piece_index: int, color: int) -> None:
        """
        Method used to handle castling movements
        :param final_piece_index: int value of piece index
        :param color: int value of color
        :return: None
        """
        if self.__current_move.get_moving_piece() == PiecesEnum.ROOK.value:
            FenUtil.disable_castling_on_side(color, self.__current_move.get_start_square(), self.__board)

        if KingUtil.is_it_castling(self.__current_move):
            self.__board.castle_king(self.__moving_piece, self.__current_move)

        elif self.__current_move.get_moving_piece() == PiecesEnum.KING.value:
            self.__board.get_fen_data().set_castling_king_side(False, color)
            self.__board.get_fen_data().set_castling_queen_side(False, color)
            self.__board.add_piece_to_the_board(self.__moving_piece, final_piece_index)
        else:
            self.__board.add_piece_to_the_board(self.__moving_piece, final_piece_index)

    def check_quit_release_event_functions(self, start_square: int, row: int, col: int, end_square: int, event) -> bool:
        """
        Method used to check conditions to end mouse event.
        """
        if self.__promotion_util.is_this_pawn_promoting():
            self.__promotion_util.check_user_choice(event, self.__canvas.get_rect_height(), self.__board)
            self.update_board_data()
            return False

        if start_square is None or row is None or col is None:
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            return False
        self.__current_move.set_end_square(row, col)

        if not self.__board.is_it_legal_move(self.__current_move) or start_square == end_square:
            self.__board.add_piece_to_the_board(self.__moving_piece, start_square)
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
            self.__canvas.copy_current_move(self.__current_move)
            self.__current_move.set_start_square(None, None)
            self.__current_move.set_end_square(None, None)
            self.update()
            return False
        return True

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
        self.__board.__init__()
        self.__current_move.set_start_square(None, None)
        self.__current_move.set_end_square(None, None)
        self.update()

    def switch_sides(self) -> None:
        """
        Method used to switch sides of player and engine (colors)
        :return: None
        """
        self.__board.switch_colors()
        self.update()
