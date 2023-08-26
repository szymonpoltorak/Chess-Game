class IllegalStateException(Exception):
    """
    Class containing exception for illegal state made during condition statements
    """

    def __init__(self, message: str):
        super(IllegalStateException, self).__init__(message)
