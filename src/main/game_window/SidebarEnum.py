from enum import Enum


class SidebarEnum(Enum):
    """
    Enum consists every SideBar needed offset value.
    """
    SIDEBAR_X: int = 0
    SIDEBAR_Y: int = 0
    SIDEBAR_WIDTH: int = 91
    SIDEBAR_HEIGHT: int = 720

    SIDEBAR_MARGIN_LEFT: int = 9
    SIDEBAR_MARGIN_TOP: int = 0
    SIDEBAR_MARGIN_RIGHT: int = 0
    SIDEBAR_MARGIN_BOTTOM: int = 0

    SIDEBAR_ICON_WIDTH: int = 60
    SIDEBAR_ICON_HEIGHT: int = 60
    SIDEBAR_ICON_FRAME_WIDTH: int = 70
    SIDEBAR_ICON_FRAME_HEIGHT: int = 70
