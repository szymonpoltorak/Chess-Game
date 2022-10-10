from enum import Enum


class BoardEnum(Enum):
    """
     Enum which covers important static values for board.
    """
    PRIMARY_BOARD_COLOR: str = "#F1D9C0"
    SECONDARY_BOARD_COLOR: str = "#A97A65"

    BOARD_LENGTH: int = 8
    BOARD_SIZE: int = 64
    NUMBER_OF_DIRECTIONS: int = 8
    CHARACTER_SIZE: int = 22

    NUMBER_SCALE_X: int = 8
    NUMBER_SCALE_Y: int = 8
    LETTER_SCALE_X: int = 70
    LETTER_SCALE_Y: int = 70

    STARTING_POSITION: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
