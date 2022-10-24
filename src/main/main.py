import sys

from PyQt5.QtWidgets import QApplication

from game_window.GameWindow import GameWindow


def main():
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()

    sys.exit(app.exec_())


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    main()
