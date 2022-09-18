import sys
from PyQt5.QtWidgets import QApplication

from game_window.GameWindow import GameWindow


def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
