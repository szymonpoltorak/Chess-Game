import sys
import pygame
from PyQt5.QtWidgets import QApplication

from game_window.PyGameEnum import PyGameEnum
from game_window.GameWindow import GameWindow


def run_chess_game():
    """
    Initializes chess game.
    :return: void
    """
    pygame.init()
    canvas = pygame.Surface((PyGameEnum.SURFACE_WIDTH.value, PyGameEnum.SURFACE_HEIGHT.value))

    app = QApplication(sys.argv)
    window = GameWindow(canvas)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run_chess_game()
