import ctypes

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from src.main.SideBar import SideBar


class GameWindowUi:
    """
    Class covers whole PyQt5 Ui except PyGame chess board.
    """
    __slots__ = ("__side_bar", "__right_container", "__pgn_table", "__button_frame", "__button_horizontal_layout",
                 "__user_frame", "__user_icon", "__user_name", "__engine_frame", "__engine_icon", "__engine_name",
                 "__new_game_button", "__prev_move_button", "__next_move_button", "__analyze_button")

    def __init__(self, game_window: QWidget):
        appid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

        game_window.setObjectName("game_window")
        game_window.resize(1300, 720)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/resources/images/chess_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        game_window.setWindowIcon(icon)
        game_window.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        game_window.setMinimumSize(QtCore.QSize(1300, 720))
        game_window.setMaximumSize(QtCore.QSize(1300, 720))

        self.__side_bar = SideBar(game_window)

        self.__right_container = QtWidgets.QFrame(game_window)
        self.__right_container.setGeometry(QtCore.QRect(780, 0, 521, 720))
        self.__right_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__right_container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__right_container.setObjectName("__right_container")

        self.__pgn_table = QtWidgets.QTableView(self.__right_container)
        self.__pgn_table.setGeometry(QtCore.QRect(20, 80, 491, 481))
        self.__pgn_table.setObjectName("__pgn_table")

        self.__init_players_profile(game_window)
        self.__init_buttons()
        self.__retranslate_ui(game_window)
        QtCore.QMetaObject.connectSlotsByName(game_window)

    def __init_players_profile(self, game_window: QWidget):
        """
        Initializes user and engine labels with their names and their icons.
        :param game_window:
        :return: void
        """
        self.__user_frame = QtWidgets.QFrame(game_window)
        self.__user_frame.setGeometry(QtCore.QRect(160, 650, 221, 51))
        self.__user_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__user_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__user_frame.setObjectName("__user_frame")

        self.__user_icon = QtWidgets.QLabel(self.__user_frame)
        self.__user_icon.setGeometry(QtCore.QRect(0, 0, 61, 51))
        self.__user_icon.setText("")
        self.__user_icon.setPixmap(QtGui.QPixmap("src/resources/images/user.png"))
        self.__user_icon.setScaledContents(True)
        self.__user_icon.setObjectName("__user_icon")

        self.__user_name = QtWidgets.QLabel(self.__user_frame)
        self.__user_name.setGeometry(QtCore.QRect(66, 12, 151, 31))
        self.__user_name.setObjectName("__user_name")

        self.__engine_frame = QtWidgets.QFrame(game_window)
        self.__engine_frame.setGeometry(QtCore.QRect(150, 20, 221, 51))
        self.__engine_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__engine_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__engine_frame.setObjectName("__engine_frame")

        self.__engine_icon = QtWidgets.QLabel(self.__engine_frame)
        self.__engine_icon.setGeometry(QtCore.QRect(0, 0, 61, 51))
        self.__engine_icon.setText("")
        self.__engine_icon.setPixmap(QtGui.QPixmap("src/resources/images/engine.svg"))
        self.__engine_icon.setScaledContents(True)
        self.__engine_icon.setObjectName("__engine_icon")

        self.__engine_name = QtWidgets.QLabel(self.__engine_frame)
        self.__engine_name.setGeometry(QtCore.QRect(66, 12, 151, 31))
        self.__engine_name.setObjectName("__engine_name")

    def __init_buttons(self):
        """
        Initializes buttons on the right frame of window.
        :return: void
        """
        self.__button_frame = QtWidgets.QFrame(self.__right_container)
        self.__button_frame.setGeometry(QtCore.QRect(10, 560, 511, 101))
        self.__button_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__button_frame.setObjectName("__button_frame")
        self.__button_horizontal_layout = QtWidgets.QHBoxLayout(self.__button_frame)
        self.__button_horizontal_layout.setObjectName("button_horizontal_layout")

        self.__new_game_button = QtWidgets.QPushButton(self.__button_frame)
        self.__new_game_button.setMinimumSize(QtCore.QSize(111, 61))
        self.__new_game_button.setObjectName("__new_game_button")
        self.__button_horizontal_layout.addWidget(self.__new_game_button)

        self.__prev_move_button = QtWidgets.QPushButton(self.__button_frame)
        self.__prev_move_button.setMinimumSize(QtCore.QSize(111, 61))
        self.__prev_move_button.setObjectName("__prev_move_button")
        self.__button_horizontal_layout.addWidget(self.__prev_move_button)

        self.__next_move_button = QtWidgets.QPushButton(self.__button_frame)
        self.__next_move_button.setMinimumSize(QtCore.QSize(111, 61))
        self.__next_move_button.setObjectName("__next_move_button")
        self.__button_horizontal_layout.addWidget(self.__next_move_button)

        self.__analyze_button = QtWidgets.QPushButton(self.__button_frame)
        self.__analyze_button.setMinimumSize(QtCore.QSize(111, 61))
        self.__analyze_button.setObjectName("__analyze_button")
        self.__button_horizontal_layout.addWidget(self.__analyze_button)

    def __retranslate_ui(self, game_window: QWidget):
        """
        Void method to retranslate ui elements.
        :param game_window: QtWidget instance
        :return: void
        """
        _translate = QtCore.QCoreApplication.translate
        game_window.setWindowTitle(_translate("game_window", "Chess Engine"))
        self.__new_game_button.setText(_translate("game_window", "New Game"))
        self.__prev_move_button.setText(_translate("game_window", "<"))
        self.__next_move_button.setText(_translate("game_window", ">"))
        self.__analyze_button.setText(_translate("game_window", "Analyze"))
        self.__user_name.setText(_translate("game_window", "User"))
        self.__engine_name.setText(_translate("game_window", "Engine"))

    def get_sidebar(self):
        """
        Method returns private SideBar instance.
        :return: SideBar field
        """
        return self.__side_bar
