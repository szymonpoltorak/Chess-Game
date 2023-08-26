class NullArgumentException(Exception):
    """
    Class containing exception for null given as arguments
    """

    def __init__(self, message: str):
        super(NullArgumentException, self).__init__(message)
