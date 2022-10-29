from numpy import array
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QWidget

from game_window.enums.Paths import Paths
from game_window.enums.SidebarEnum import SidebarEnum


class Sidebar:
    """
    Class containing whole sidebar and their icons.
    """

    __slots__ = array(["__side_bar", "__side_bar_vertical_layout", "__settings_frame", "__settings_horizontal_layout",
                       "__settings_menu", "__play_frame", "__play_horizontal_layout", "__play_menu", "__analysis_frame",
                       "__analyze_horizontal_layout", "__analysis_menu", "__profile_frame",
                       "__profile_horizontal_layout", "__profile_menu", "__players_frame",
                       "__players_horizontal_layout", "__players_menu"], dtype=str)

    def __init__(self, game_window: QWidget):
        self.__side_bar = QtWidgets.QFrame(game_window)
        self.__side_bar.setGeometry(QtCore.QRect(SidebarEnum.SIDEBAR_X.value, SidebarEnum.SIDEBAR_Y.value,
                                                 SidebarEnum.SIDEBAR_WIDTH.value, SidebarEnum.SIDEBAR_HEIGHT.value))
        self.__side_bar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.__side_bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__side_bar.setObjectName("__side_bar")

        self.__side_bar_vertical_layout = QtWidgets.QVBoxLayout(self.__side_bar)
        self.__side_bar_vertical_layout.setContentsMargins(SidebarEnum.SIDEBAR_MARGIN_LEFT.value,
                                                           SidebarEnum.SIDEBAR_MARGIN_TOP.value,
                                                           SidebarEnum.SIDEBAR_MARGIN_RIGHT.value,
                                                           SidebarEnum.SIDEBAR_MARGIN_BOTTOM.value)
        self.__side_bar_vertical_layout.setObjectName("side_bar_vertical_layout")

        self.__init_play()
        self.__init_analysis()
        self.__init_players()
        self.__init_profile()
        self.__init_settings()

    def __init_settings(self):
        """
        Initializes settings menu option and its icon.
        :return: None
        """
        self.__settings_frame = QtWidgets.QFrame(self.__side_bar)
        self.__frame_menu_first_setup(self.__settings_frame)

        self.__settings_frame.setObjectName("__settings_frame")
        self.__settings_horizontal_layout = QtWidgets.QHBoxLayout(self.__settings_frame)
        self.__settings_horizontal_layout.setObjectName("settings_horizontal_layout")

        self.__settings_menu = QtWidgets.QLabel(self.__settings_frame)
        self.__settings_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__settings_menu.setMaximumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_WIDTH.value,
                                                         SidebarEnum.SIDEBAR_ICON_HEIGHT.value))
        self.__settings_menu.setPixmap(QtGui.QPixmap(Paths.SETTINGS_ICON.value))
        self.__settings_menu.setScaledContents(True)
        self.__settings_menu.setObjectName("__settings_menu")
        self.__settings_horizontal_layout.addWidget(self.__settings_menu)
        self.__settings_menu.setToolTip("Settings")
        self.__side_bar_vertical_layout.addWidget(self.__settings_frame)

    def __init_play(self):
        """
        Initializes play menu option and its icon.
        :return: None
        """
        self.__play_frame = QtWidgets.QFrame(self.__side_bar)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.__play_frame.sizePolicy().hasHeightForWidth())

        self.__play_frame.setSizePolicy(size_policy)
        self.__frame_menu_first_setup(self.__play_frame)

        self.__play_frame.setObjectName("__play_frame")
        self.__play_horizontal_layout = QtWidgets.QHBoxLayout(self.__play_frame)
        self.__play_horizontal_layout.setObjectName("play_horizontal_layout")

        self.__play_menu = QtWidgets.QLabel(self.__play_frame)
        self.__play_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__play_menu.setMaximumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_WIDTH.value,
                                                     SidebarEnum.SIDEBAR_ICON_HEIGHT.value))
        self.__play_menu.setPixmap(QtGui.QPixmap(Paths.PLAY_ICON.value))
        self.__play_menu.setScaledContents(True)
        self.__play_menu.setObjectName("__play_menu")
        self.__play_menu.setToolTip("Play a game")
        self.__play_horizontal_layout.addWidget(self.__play_menu)
        self.__side_bar_vertical_layout.addWidget(self.__play_frame)

    def __init_analysis(self):
        """
        Initializes analysis menu option and its icon.
        :return: None
        """
        self.__analysis_frame = QtWidgets.QFrame(self.__side_bar)
        self.__frame_menu_first_setup(self.__analysis_frame)

        self.__analysis_frame.setObjectName("__analysis_frame")
        self.__analyze_horizontal_layout = QtWidgets.QHBoxLayout(self.__analysis_frame)
        self.__analyze_horizontal_layout.setObjectName("analyze_horizontal_layout")

        self.__analysis_menu = QtWidgets.QLabel(self.__analysis_frame)
        self.__analysis_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__analysis_menu.setMaximumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_WIDTH.value,
                                                         SidebarEnum.SIDEBAR_ICON_HEIGHT.value))
        self.__analysis_menu.setPixmap(QtGui.QPixmap(Paths.ANALYSIS_ICON.value))
        self.__analysis_menu.setScaledContents(True)
        self.__analysis_menu.setObjectName("__analysis_menu")
        self.__analysis_menu.setToolTip("Analyze Parties")
        self.__analyze_horizontal_layout.addWidget(self.__analysis_menu)
        self.__side_bar_vertical_layout.addWidget(self.__analysis_frame)

    def __init_profile(self):
        """
        Initializes profile menu option and its icon.
        :return: None
        """
        self.__profile_frame = QtWidgets.QFrame(self.__side_bar)
        self.__frame_menu_first_setup(self.__profile_frame)

        self.__profile_frame.setObjectName("__profile_frame")
        self.__profile_horizontal_layout = QtWidgets.QHBoxLayout(self.__profile_frame)
        self.__profile_horizontal_layout.setObjectName("profile_horizontal_layout")

        self.__profile_menu = QtWidgets.QLabel(self.__profile_frame)
        self.__profile_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__profile_menu.setMaximumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_WIDTH.value,
                                                        SidebarEnum.SIDEBAR_ICON_HEIGHT.value))
        self.__profile_menu.setPixmap(QtGui.QPixmap(Paths.PROFILE_ICON.value))
        self.__profile_menu.setScaledContents(True)
        self.__profile_menu.setObjectName("__profile_menu")
        self.__profile_menu.setToolTip("Your Profile")
        self.__profile_horizontal_layout.addWidget(self.__profile_menu)
        self.__side_bar_vertical_layout.addWidget(self.__profile_frame)

    def __init_players(self):
        """
        Initializes players menu option and its icon.
        :return: None
        """
        self.__players_frame = QtWidgets.QFrame(self.__side_bar)
        self.__frame_menu_first_setup(self.__players_frame)

        self.__players_frame.setObjectName("__players_frame")
        self.__players_horizontal_layout = QtWidgets.QHBoxLayout(self.__players_frame)
        self.__players_horizontal_layout.setObjectName("players_horizontal_layout")

        self.__players_menu = QtWidgets.QLabel(self.__players_frame)
        self.__players_menu.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.__players_menu.setMaximumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_WIDTH.value,
                                                        SidebarEnum.SIDEBAR_ICON_HEIGHT.value))
        self.__players_menu.setPixmap(QtGui.QPixmap(Paths.PLAYERS_ICON.value))
        self.__players_menu.setScaledContents(True)
        self.__players_menu.setObjectName("__players_menu")
        self.__players_menu.setToolTip("Player array")
        self.__players_horizontal_layout.addWidget(self.__players_menu)
        self.__side_bar_vertical_layout.addWidget(self.__players_frame)

    def __frame_menu_first_setup(self, frame: QFrame):
        frame.setMinimumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_FRAME_WIDTH.value,
                                          SidebarEnum.SIDEBAR_ICON_FRAME_HEIGHT.value))
        frame.setMaximumSize(QtCore.QSize(SidebarEnum.SIDEBAR_ICON_FRAME_WIDTH.value,
                                          SidebarEnum.SIDEBAR_ICON_FRAME_HEIGHT.value))
        frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
