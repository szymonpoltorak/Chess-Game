import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

from game_window.GameWindow import GameWindow


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    window: QWidget = GameWindow()
    window.show()

    sys.exit(app.exec_())


def except_hook(cls, exception, traceback) -> None:
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    main()
