from numpy import ndarray, array

from game_window.enums.PiecesEnum import PiecesEnum


class BoardInitializer:
    @staticmethod
    def init_black_pieces_array() -> ndarray[int]:
        """
        Initializes array of pieces on starting position depending on given color value.
        :return: array of starting pieces of given color
        """
        piece_array = array([PiecesEnum.BLACK.value | PiecesEnum.ROOK.value,
                             PiecesEnum.BLACK.value | PiecesEnum.KNIGHT.value,
                             PiecesEnum.BLACK.value | PiecesEnum.BISHOP.value,
                             PiecesEnum.BLACK.value | PiecesEnum.QUEEN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.KING.value,
                             PiecesEnum.BLACK.value | PiecesEnum.BISHOP.value,
                             PiecesEnum.BLACK.value | PiecesEnum.KNIGHT.value,
                             PiecesEnum.BLACK.value | PiecesEnum.ROOK.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value,
                             PiecesEnum.BLACK.value | PiecesEnum.PAWN.value])
        return piece_array

    @staticmethod
    def init_white_pieces_array() -> ndarray[int]:
        """
        Initializes array of pieces on starting position depending on given color value.
        :return: array of starting pieces of given color
        """
        return array([PiecesEnum.WHITE.value | PiecesEnum.ROOK.value,
                      PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value,
                      PiecesEnum.WHITE.value | PiecesEnum.BISHOP.value,
                      PiecesEnum.WHITE.value | PiecesEnum.KING.value,
                      PiecesEnum.WHITE.value | PiecesEnum.QUEEN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.BISHOP.value,
                      PiecesEnum.WHITE.value | PiecesEnum.KNIGHT.value,
                      PiecesEnum.WHITE.value | PiecesEnum.ROOK.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value,
                      PiecesEnum.WHITE.value | PiecesEnum.PAWN.value])
