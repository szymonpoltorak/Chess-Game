from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget


class SideBar:
    """
    Class containing whole sidebar and their icons.
    """

    __slots__ = ("__side_bar", "__side_bar_vertical_layout", "__settings_frame", "__settings_horizontal_layout",
                 "__settings_menu", "__play_frame", "__play_horizontal_layout", "__play_menu", "__analysis_frame",
                 "__analyze_horizontal_layout", "__analysis_menu", "__profile_frame", "__profile_horizontal_layout",
                 "__profile_menu", "__players_frame", "__players_horizontal_layout", "__players_menu")

    def __init__(self, game_window: QWidget):
        self.__side_bar = QtWidgets.QFrame(game_window)
        self.__side_bar.setGeometry(QtCore.QRect(0, 0, 91, 721))
        self.__side_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__side_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__side_bar.setObjectName("__side_bar")

        self.__side_bar_vertical_layout = QtWidgets.QVBoxLayout(self.__side_bar)
        self.__side_bar_vertical_layout.setContentsMargins(9, 0, 0, 0)
        self.__side_bar_vertical_layout.setObjectName("side_bar_vertical_layout")

        self.__init_play()
        self.__init_analysis()
        self.__init_players()
        self.__init_settings()
        self.__init_profile()

    def __init_settings(self):
        """
        Initializes settings menu option and its icon.
        :return: void
        """
        self.__settings_frame = QtWidgets.QFrame(self.__side_bar)
        self.__settings_frame.setMinimumSize(QtCore.QSize(70, 70))
        self.__settings_frame.setMaximumSize(QtCore.QSize(70, 70))
        self.__settings_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__settings_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__settings_frame.setObjectName("__settings_frame")
        self.__settings_horizontal_layout = QtWidgets.QHBoxLayout(self.__settings_frame)
        self.__settings_horizontal_layout.setObjectName("settings_horizontal_layout")

        self.__settings_menu = QtWidgets.QLabel(self.__settings_frame)
        self.__settings_menu.setMaximumSize(QtCore.QSize(60, 60))
        self.__settings_menu.setText("")
        self.__settings_menu.setPixmap(QtGui.QPixmap("src/resources/images/settings.svg"))
        self.__settings_menu.setScaledContents(True)
        self.__settings_menu.setObjectName("__settings_menu")
        self.__settings_horizontal_layout.addWidget(self.__settings_menu)
        self.__side_bar_vertical_layout.addWidget(self.__settings_frame)

    def __init_play(self):
        """
        Initializes play menu option and its icon.
        :return: void
        """
        self.__play_frame = QtWidgets.QFrame(self.__side_bar)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.__play_frame.sizePolicy().hasHeightForWidth())

        self.__play_frame.setSizePolicy(size_policy)
        self.__play_frame.setMinimumSize(QtCore.QSize(70, 70))
        self.__play_frame.setMaximumSize(QtCore.QSize(70, 70))
        self.__play_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__play_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__play_frame.setObjectName("__play_frame")
        self.__play_horizontal_layout = QtWidgets.QHBoxLayout(self.__play_frame)
        self.__play_horizontal_layout.setObjectName("play_horizontal_layout")

        self.__play_menu = QtWidgets.QLabel(self.__play_frame)
        self.__play_menu.setMaximumSize(QtCore.QSize(60, 60))
        self.__play_menu.setText("")
        self.__play_menu.setPixmap(QtGui.QPixmap("src/resources/images/play.svg"))
        self.__play_menu.setScaledContents(True)
        self.__play_menu.setObjectName("__play_menu")
        self.__play_horizontal_layout.addWidget(self.__play_menu)
        self.__side_bar_vertical_layout.addWidget(self.__play_frame)

    def __init_analysis(self):
        """
        Initializes analysis menu option and its icon.
        :return: void
        """
        self.__analysis_frame = QtWidgets.QFrame(self.__side_bar)
        self.__analysis_frame.setMinimumSize(QtCore.QSize(70, 70))
        self.__analysis_frame.setMaximumSize(QtCore.QSize(70, 70))
        self.__analysis_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__analysis_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__analysis_frame.setObjectName("__analysis_frame")
        self.__analyze_horizontal_layout = QtWidgets.QHBoxLayout(self.__analysis_frame)
        self.__analyze_horizontal_layout.setObjectName("analyze_horizontal_layout")

        self.__analysis_menu = QtWidgets.QLabel(self.__analysis_frame)
        self.__analysis_menu.setMaximumSize(QtCore.QSize(60, 60))
        self.__analysis_menu.setText("")
        self.__analysis_menu.setPixmap(QtGui.QPixmap("src/resources/images/analysis.svg"))
        self.__analysis_menu.setScaledContents(True)
        self.__analysis_menu.setObjectName("__analysis_menu")
        self.__analyze_horizontal_layout.addWidget(self.__analysis_menu)
        self.__side_bar_vertical_layout.addWidget(self.__analysis_frame)

    def __init_profile(self):
        """
        Initializes profile menu option and its icon.
        :return: void
        """
        self.__profile_frame = QtWidgets.QFrame(self.__side_bar)
        self.__profile_frame.setMinimumSize(QtCore.QSize(70, 70))
        self.__profile_frame.setMaximumSize(QtCore.QSize(70, 70))
        self.__profile_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__profile_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__profile_frame.setObjectName("__profile_frame")
        self.__profile_horizontal_layout = QtWidgets.QHBoxLayout(self.__profile_frame)
        self.__profile_horizontal_layout.setObjectName("profile_horizontal_layout")

        self.__profile_menu = QtWidgets.QLabel(self.__profile_frame)
        self.__profile_menu.setMaximumSize(QtCore.QSize(60, 60))
        self.__profile_menu.setText("")
        self.__profile_menu.setPixmap(QtGui.QPixmap("src/resources/images/profile.svg"))
        self.__profile_menu.setScaledContents(True)
        self.__profile_menu.setObjectName("__profile_menu")
        self.__profile_horizontal_layout.addWidget(self.__profile_menu)
        self.__side_bar_vertical_layout.addWidget(self.__profile_frame)

    def __init_players(self):
        """
        Initializes players menu option and its icon.
        :return: void
        """
        self.__players_frame = QtWidgets.QFrame(self.__side_bar)
        self.__players_frame.setMinimumSize(QtCore.QSize(70, 70))
        self.__players_frame.setMaximumSize(QtCore.QSize(70, 70))
        self.__players_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__players_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__players_frame.setObjectName("__players_frame")
        self.__players_horizontal_layout = QtWidgets.QHBoxLayout(self.__players_frame)
        self.__players_horizontal_layout.setObjectName("players_horizontal_layout")

        self.__players_menu = QtWidgets.QLabel(self.__players_frame)
        self.__players_menu.setMaximumSize(QtCore.QSize(60, 60))
        self.__players_menu.setText("")
        self.__players_menu.setPixmap(QtGui.QPixmap("src/resources/images/players.svg"))
        self.__players_menu.setScaledContents(True)
        self.__players_menu.setObjectName("__players_menu")
        self.__players_horizontal_layout.addWidget(self.__players_menu)
        self.__side_bar_vertical_layout.addWidget(self.__players_frame)
