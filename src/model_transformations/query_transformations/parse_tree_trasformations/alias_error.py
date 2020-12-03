class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class AliasNameError(Error):
    """
    When the compostion of relationships is not defined, this error is raised.
    """

    def __init__(self, message):
        self.message = message