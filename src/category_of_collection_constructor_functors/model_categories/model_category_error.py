class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class ModelRelationshipCompositionError(Error):
    """
    When the compostion of relationships is not defined, this error is raised.
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message