from enum import Enum


class GameWindowEnum(Enum):
    """
    GameWindowEnum contains static values for GameWindow.
    """
    WINDOW_WIDTH: int = 1300
    WINDOW_HEIGHT: int = 720

    RIGHT_CONTAINER_X: int = 780
    RIGHT_CONTAINER_Y: int = 0
    RIGHT_CONTAINER_WIDTH: int = 521
    RIGHT_CONTAINER_HEIGHT: int = 720

    PGN_TABLE_X: int = 20
    PGN_TABLE_Y: int = 80
    PGN_TABLE_WIDTH: int = 491
    PGN_TABLE_HEIGHT: int = 481

    BUTTON_FRAME_A_LEFT: int = 10
    BUTTON_FRAME_A_TOP: int = 560
    BUTTON_FRAME_A_WIDTH: int = 511
    BUTTON_FRAME_A_HEIGHT: int = 111

    BUTTON_WIDTH: int = 111
    BUTTON_HEIGHT: int = 61

    USER_FRAME_X: int = 160
    USER_FRAME_Y: int = 650
    USER_FRAME_WIDTH: int = 221
    USER_FRAME_HEIGHT: int = 51

    USER_ICON_X: int = 0
    USER_ICON_Y: int = 0
    USER_ICON_WIDTH: int = 61
    USER_ICON_HEIGHT: int = 51

    USER_NAME_X: int = 66
    USER_NAME_Y: int = 12
    USER_NAME_WIDTH: int = 151
    USER_NAME_HEIGHT: int = 31

    ENGINE_FRAME_X: int = 150
    ENGINE_FRAME_Y: int = 20
    ENGINE_FRAME_WIDTH: int = 221
    ENGINE_FRAME_HEIGHT: int = 51

    ENGINE_ICON_X: int = 0
    ENGINE_ICON_Y: int = 0
    ENGINE_ICON_WIDTH: int = 61
    ENGINE_ICON_HEIGHT: int = 51

    ENGINE_NAME_X: int = 66
    ENGINE_NAME_Y: int = 12
    ENGINE_NAME_WIDTH: int = 151
    ENGINE_NAME_HEIGHT: int = 31
