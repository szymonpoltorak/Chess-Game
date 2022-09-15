import sys
import pygame
from PyQt5.QtWidgets import QApplication

from game_window.PyGameEnum import PyGameEnum
from game_window.GameWindow import GameWindow


if __name__ == '__main__':
    pygame.init()
    surface = pygame.Surface((PyGameEnum.SURFACE_WIDTH.value, PyGameEnum.SURFACE_HEIGHT.value))

    app = QApplication(sys.argv)
    window = GameWindow(surface)
    window.show()

    sys.exit(app.exec_())
