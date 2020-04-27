class InstanceFunctor:
    """
    Instance functor is a mapping from the Instance category to Schema category. The idea is that is describes the current state of the database. 
    It is sort of data forgetting function in the sense that it forgets the concrete data when it maps from Instance to Schema.
    """

    def __init__(self, instanceCategory):
        self.instanceCategory = instanceCategory