from numpy import array
from numpy import dtype
from numpy import generic
from numpy import ndarray
from PyQt5.QtCore import QRect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QStaticText

from game_window.board.Board import Board
from game_window.ColorManager import ColorManager
from game_window.enums.BoardEnum import BoardEnum
from game_window.enums.CanvasEnum import CanvasEnum
from game_window.enums.MoveEnum import MoveEnum
from game_window.enums.Paths import Paths
from game_window.enums.PiecesEnum import PiecesEnum
from game_window.moving.generation.data.Move import Move
from game_window.PromotionData import PromotionData
from Promoter import Promoter


class Canvas(QPainter):
    """
    Class which manages painting board and pieces.
    """
    __slots__ = array(["__rect_width", "__rect_height", "__freeze_piece", "__freeze_start", "__freeze_end"],
                      dtype=str)

    def __init__(self) -> None:
        super(Canvas, self).__init__()
        self.__rect_width = int(CanvasEnum.CANVAS_WIDTH.value / 8)
        self.__rect_height = int(CanvasEnum.CANVAS_HEIGHT.value / 8)
        self.__freeze_piece = -1
        self.__freeze_start = -1
        self.__freeze_end = -1

    def draw_chess_board(self, move: Move, board: Board) -> None:
        """
        Method draws a whole chess board on canvas.
        :return: None
        """
        current_x = CanvasEnum.CANVAS_X.value
        current_y = CanvasEnum.CANVAS_Y.value
        index_x = CanvasEnum.CANVAS_X.value
        index_y = CanvasEnum.CANVAS_Y.value

        current_number = 8
        letters = ("a", "b", "c", "d", "e", "f", "g", "h")

        for row in range(BoardEnum.BOARD_LENGTH.value):
            for col in range(BoardEnum.BOARD_LENGTH.value):
                color: str = ColorManager.pick_proper_color(row, col)
                rectangle = QRect(current_x, current_y, self.__rect_width, self.__rect_height)
                current_square = BoardEnum.BOARD_LENGTH.value * row + col

                if move.get_start_square() == move.get_end_square():
                    self.fillRect(rectangle, QColor(color))
                elif move.get_start_square() == current_square:
                    self.fillRect(rectangle, QColor(MoveEnum.START_SQUARE_COLOR.value))
                elif move.get_end_square() == current_square:
                    self.fillRect(rectangle, QColor(MoveEnum.END_SQUARE_COLOR.value))
                else:
                    self.fillRect(rectangle, QColor(color))
                current_x += self.__rect_width

                if col == CanvasEnum.FIRST_COLUMN.value:
                    self.draw_character_on_board(current_number, index_x + BoardEnum.NUMBER_SCALE_X.value,
                                                 index_y + BoardEnum.NUMBER_SCALE_Y.value,
                                                 ColorManager.get_opposite_square_color(color))
                    current_number -= 1
                if row == CanvasEnum.LAST_ROW.value:
                    self.draw_character_on_board(letters[col], index_x + BoardEnum.LETTER_SCALE_X.value,
                                                 index_y + BoardEnum.LETTER_SCALE_Y.value,
                                                 ColorManager.get_opposite_square_color(color))
                    index_x = current_x
            current_y += self.__rect_height
            current_x = CanvasEnum.CANVAS_X.value
            index_y = current_y
        self.paint_possible_moves_for_frozen_piece(board)
        self.__draw_position_from_fen(board)

    def draw_character_on_board(self, character: int | str, position_x: int, position_y: int, color: str) -> None:
        """
        Draw characters : number and letters on board edges.
        :param character: characters string which we want to paint on canvas
        :param position_x: x coordinate where we want to start drawing character
        :param position_y: y coordinate where we want to start drawing character
        :param color: color string which we want a character to have
        :return: None
        """
        font = QFont("Monospace")
        font.setBold(True)

        self.setPen(QColor(color))
        self.setFont(QFont(font))
        self.drawStaticText(position_x, position_y, QStaticText(str(character)))

    def paint_promotion_window(self, data: Promoter, current_square: int) -> None:
        """
        Method used to paint promotion window for pawn
        :param data: PromotionData instance containing needed data
        :param current_square: int value of end_square
        :return: None
        """
        col = current_square % 8
        row = int((current_square - col) / 8)
        square_y = row * self.__rect_height + CanvasEnum.CANVAS_Y.value
        square_x = col * self.__rect_width + CanvasEnum.CANVAS_X.value

        if row == 0:
            square_y = row * self.__rect_height + CanvasEnum.CANVAS_Y.value
        elif row == 7:
            square_y = row * self.__rect_height + CanvasEnum.CANVAS_Y.value - 3 * self.__rect_height
        data.set_promotion_data(data.get_piece_color(), square_x, square_y, data.get_pawn_square())

        for i in range(4):
            rectangle = QRect(square_x, square_y, self.__rect_width, self.__rect_height)

            if i % 2 == 0:
                self.fillRect(rectangle, QColor("#4c5052"))
            else:
                self.fillRect(rectangle, QColor("#8b969e"))
            self.load_proper_image(square_x, square_y, self.get_promotion_piece_letter(i, data.get_piece_color()))
            square_y += self.__rect_height

    def get_promotion_piece_letter(self, index: int, color: int) -> str:
        """
        Method used to get letter of a piece with proper case
        :param index: int index of letter
        :param color: int value of color
        :return: str
        """
        letters: ndarray[str, dtype[generic]] = array(["q", "b", "n", "r"], dtype=str)

        if color == PiecesEnum.WHITE.value:
            big_letter: str = letters[index].upper()
            return big_letter
        small_letter: str = letters[index]

        return small_letter

    def __draw_position_from_fen(self, board: Board) -> None:
        """
        Method draws pieces on chess board from fen string representation.
        :return: None
        """
        fen = board.fen_string().replace('/', ' ').split()
        current_x = CanvasEnum.CANVAS_X.value
        current_y = CanvasEnum.CANVAS_Y.value

        for row in range(BoardEnum.BOARD_LENGTH.value):
            row_pieces = [*fen[row]]

            for col in range(len(row_pieces)):
                current_x = self.load_proper_image(current_x, current_y, row_pieces[col])
            current_x = CanvasEnum.CANVAS_X.value
            current_y += self.__rect_height

    def load_proper_image(self, current_x: int, current_y: int, piece_letter: str) -> int:
        """
        Loads pixmap from resources based on current letter loaded from fen string.
        :param current_x: current x coordinate from which we start drawing.
        :param current_y: current y coordinate from which we start drawing.
        :param piece_letter: letter representing piece_square on chess board, got from fen string.
        :return: x coordinate of current end_square
        """
        try:
            blank_spaces = int(piece_letter)
            current_x += blank_spaces * self.__rect_width

            return current_x
        except ValueError:
            piece = piece_letter.upper()
            pieces_path = Paths.PIECES_PATH.value
            extension = ".png"

            if piece_letter.isupper():
                color = "w"
            else:
                color = "b"
            pixmap = QPixmap(f"{pieces_path}{color}{piece}{extension}")
            pixmap = pixmap.scaledToHeight(PiecesEnum.SCALE_HEIGHT.value, Qt.SmoothTransformation)
            pixmap = pixmap.scaledToWidth(PiecesEnum.SCALE_WIDTH.value, Qt.SmoothTransformation)

            self.drawPixmap(PiecesEnum.SCALE_X.value + current_x, PiecesEnum.SCALE_Y.value + current_y,
                            PiecesEnum.SCALE_WIDTH.value, PiecesEnum.SCALE_HEIGHT.value, pixmap)
            current_x += self.__rect_width

            return current_x

    def paint_possible_moves_for_frozen_piece(self, board: Board) -> None:
        """
        Method to paint possible moves_list for not moven piece_square on board
        :return: None
        """
        current_x = CanvasEnum.CANVAS_X.value
        current_y = CanvasEnum.CANVAS_Y.value

        for row in range(BoardEnum.BOARD_LENGTH.value):
            if not self.is_it_frozen_piece():
                break
            for col in range(BoardEnum.BOARD_LENGTH.value):
                current_square = BoardEnum.BOARD_LENGTH.value * row + col
                legal_moves = board.legal_moves()

                for legal_move in legal_moves:
                    if legal_move is None:
                        break
                    if self.is_it_frozen_piece_target_square(legal_move, current_square):
                        rectangle = QRect(current_x, current_y, self.__rect_width, self.__rect_height)
                        self.fillRect(rectangle, QColor(ColorManager.get_legal_move_color(row, col)))
                        break
                current_x += self.__rect_width
            current_y += self.__rect_height
            current_x = CanvasEnum.CANVAS_X.value
        self.__freeze_piece = -1
        self.__freeze_start = -1
        self.__freeze_end = -1

    def is_it_frozen_piece(self) -> bool:
        """
        Method used to check if piece_square was not moved at all
        :return: bool value
        """
        return self.__freeze_start != -1 and self.__freeze_end != -1

    def is_it_frozen_piece_target_square(self, legal_move: Move, current_square: int) -> bool:
        """
        Methods checks if current end_square is a valid move for a frozen piece_square
        :param legal_move: current legal move instance
        :param current_square: int index of current end_square
        :return: bool value
        """
        if legal_move.get_end_square() != current_square or legal_move.get_moving_piece() != self.__freeze_piece:
            return False
        return legal_move.get_start_square() == self.__freeze_start

    def copy_current_move(self, move: Move) -> None:
        """
        Method copies values of a current move
        :param move: current move (Move instance)
        :return: None
        """
        self.__freeze_piece = move.get_moving_piece()
        self.__freeze_start = move.get_start_square()
        self.__freeze_end = move.get_end_square()

    def get_rect_width(self) -> int:
        """
        Gives access to single board rectangle width
        :return: int value of rectangle width
        """
        return self.__rect_width

    def get_rect_height(self) -> int:
        """
        Gives access to single board rectangle height
        :return: int value of rectangle height
        """
        return self.__rect_height
