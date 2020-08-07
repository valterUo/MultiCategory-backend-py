class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class GraphJoinError(Error):
    """Exception raised for errors when joining graph stuctures need pattern.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class GraphRelationalJoinError(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message