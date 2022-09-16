from enum import Enum


class GameWindowEnum(Enum):
    """
    GameWindowEnum contains static values for GameWindow.
    """
    WINDOW_WIDTH: int = 1400
    WINDOW_HEIGHT: int = 800

    RIGHT_CONTAINER_X: int = 850
    RIGHT_CONTAINER_Y: int = 0
    RIGHT_CONTAINER_WIDTH: int = 550
    RIGHT_CONTAINER_HEIGHT: int = 800

    PGN_TABLE_X: int = 20
    PGN_TABLE_Y: int = 55
    PGN_TABLE_WIDTH: int = 520
    PGN_TABLE_HEIGHT: int = 600

    BUTTON_FRAME_A_LEFT: int = 10
    BUTTON_FRAME_A_TOP: int = 665
    BUTTON_FRAME_A_WIDTH: int = 511
    BUTTON_FRAME_A_HEIGHT: int = 111

    BUTTON_WIDTH: int = 111
    BUTTON_HEIGHT: int = 61

    USER_FRAME_X: int = 150
    USER_FRAME_Y: int = 755
    USER_FRAME_WIDTH: int = 200
    USER_FRAME_HEIGHT: int = 40

    USER_ICON_X: int = 0
    USER_ICON_Y: int = 0
    USER_ICON_WIDTH: int = 40
    USER_ICON_HEIGHT: int = 40

    USER_NAME_X: int = 66
    USER_NAME_Y: int = 6
    USER_NAME_WIDTH: int = 151
    USER_NAME_HEIGHT: int = 31

    ENGINE_FRAME_X: int = 150
    ENGINE_FRAME_Y: int = 10
    ENGINE_FRAME_WIDTH: int = 200
    ENGINE_FRAME_HEIGHT: int = 40

    ENGINE_ICON_X: int = 0
    ENGINE_ICON_Y: int = 0
    ENGINE_ICON_WIDTH: int = 40
    ENGINE_ICON_HEIGHT: int = 40

    ENGINE_NAME_X: int = 66
    ENGINE_NAME_Y: int = 6
    ENGINE_NAME_WIDTH: int = 151
    ENGINE_NAME_HEIGHT: int = 31
