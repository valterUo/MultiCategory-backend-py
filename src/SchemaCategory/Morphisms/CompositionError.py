class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class CompositionError(Error):
    """Exception raised for errors in the composition of morphisms when source and target objects are not match.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message