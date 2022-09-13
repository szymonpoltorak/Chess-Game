import sys
import pygame
from PyQt5.QtWidgets import QApplication

from src.main.GameWindow import GameWindow

if __name__ == '__main__':
    pygame.init()
    canvas = pygame.Surface((640, 560))

    app = QApplication(sys.argv)

    window = GameWindow(canvas)
    window.show()

    sys.exit(app.exec_())
