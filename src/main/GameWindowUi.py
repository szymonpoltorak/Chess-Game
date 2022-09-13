from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes

from src.main import GameWindow


class GameWindowUi(object):
    __slots__ = ("__pgn_table", "__new_game_button", "__prev_move_button", "__next_move_button", "__analyze_button")

    def __init__(self, game_window: GameWindow):
        appid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

        game_window.setObjectName("GameWindow")
        game_window.resize(1280, 720)
        game_window.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))

        icon = QtGui.QIcon("src/resources/images/chess_icon.png")
        icon.addPixmap(QtGui.QPixmap("src/resources/images/chess_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        game_window.setWindowIcon(icon)

        self.__pgn_table = QtWidgets.QTableView(game_window)
        self.__pgn_table.setGeometry(QtCore.QRect(770, 80, 491, 481))
        self.__pgn_table.setObjectName("pgn_table")

        self.__init_buttons(game_window)
        self.__retranslate_ui(game_window)

        QtCore.QMetaObject.connectSlotsByName(game_window)

    def __retranslate_ui(self, game_window: GameWindow):
        _translate = QtCore.QCoreApplication.translate
        game_window.setWindowTitle(_translate("GameWindow", "Chess Engine"))

        self.__new_game_button.setText(_translate("GameWindow", "New Game"))
        self.__prev_move_button.setText(_translate("GameWindow", "<"))
        self.__next_move_button.setText(_translate("GameWindow", ">"))
        self.__analyze_button.setText(_translate("GameWindow", "Analyze"))

    def __init_buttons(self, game_window: GameWindow):
        self.__new_game_button = QtWidgets.QPushButton(game_window)
        self.__new_game_button.setGeometry(QtCore.QRect(770, 580, 111, 61))
        self.__new_game_button.setObjectName("new_game_button")

        self.__prev_move_button = QtWidgets.QPushButton(game_window)
        self.__prev_move_button.setGeometry(QtCore.QRect(900, 580, 111, 61))
        self.__prev_move_button.setObjectName("prev_move_button")

        self.__next_move_button = QtWidgets.QPushButton(game_window)
        self.__next_move_button.setGeometry(QtCore.QRect(1030, 580, 111, 61))
        self.__next_move_button.setObjectName("next_move_button")

        self.__analyze_button = QtWidgets.QPushButton(game_window)
        self.__analyze_button.setGeometry(QtCore.QRect(1150, 580, 111, 61))
        self.__analyze_button.setObjectName("analyze_button")
