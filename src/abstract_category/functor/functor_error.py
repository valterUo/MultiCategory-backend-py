class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class FunctorError(Error):
    """
    Error raised if the given function between the domain and target categories does not satisfy the definition of functor. 
    """

    def __init__(self, message):
        self.message = message