class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class CompositionError(Error):
    """
    When the compostion of abstract morphisms is not defined, this error is raised.
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message