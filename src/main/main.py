import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget

from src.main.game_window.GameWindow import GameWindow
from src.main.game_window.init_factory.GameWindowInit import GameWindowInit


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    window: QWidget = GameWindow(GameWindowInit())
    window.show()

    sys.exit(app.exec_())


def except_hook(cls, exception, traceback) -> None:
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    main()
