from enum import Enum


class Paths(Enum):
    """
    Enum containing paths used in game window and sidebar
    """
    GAME_WINDOW_CSS: str = "src/resources/styles/GameWindow.min.css"
    PIECES_PATH: str = "src/resources/images/pieces/"
    MOVE_SOUND: str = "src/resources/sounds/Move.mp3"
    CAPTURE_SOUND: str = "src/resources/sounds/Capture.mp3"
    SETTINGS_ICON: str = "src/resources/images/ui_icons/settings.svg"
    WINDOW_ICON: str = "src/resources/images/ui_icons/chess_icon.png"
    USER_ICON: str = "src/resources/images/ui_icons/user.png"
    ENGINE_ICON: str = "src/resources/images/ui_icons/engine.svg"
    PLAY_ICON: str = "src/resources/images/ui_icons/play.svg"
    ANALYSIS_ICON: str = "src/resources/images/ui_icons/analysis.svg"
    PROFILE_ICON: str = "src/resources/images/ui_icons/profile.svg"
    PLAYERS_ICON: str = "src/resources/images/ui_icons/players.svg"
