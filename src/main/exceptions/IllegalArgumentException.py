class IllegalArgumentException(Exception):
    """
    Class containing exception for illegal arguments given as arguments
    """

    def __init__(self, message: str):
        super(IllegalArgumentException, self).__init__(message)
