class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class DataTransformationError(Error):

    def __init__(self, message, expression):
        self.message = message
        self.expression = expression