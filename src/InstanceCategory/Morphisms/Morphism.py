class Morphism:

    """
    Morhisms in the instance category have been expanded so that they are relations between different data collections i.e. objects in the category.
    This naturally includes all the functions between data collections. Composition is defined as composition of relations and this concise with the
    definition of composition of functions.

    With relations it is easier to model many-to-many kind of relationships in multi-model data.

    If the relation is function between the source object and target object, then functional parameter is true otherwise it is false. Certain category
    theoretical constructions require functions.

    The relation parameter can be defined as a function that takes an element from sourceObject and identifies some amount of objects from the target object.
    The relation is a subset of source object x target object where we consider source and target objects suitable as sets of elements from the collections
    which are stored in the objects.

    The composition function in this class needs to satisfy the compostion rule of relation: the composition of relations R : A -> B and S : B -> C is S o R where a(S o R)c
    if there exists such b in B that aSb and bRc.
    """

    def __init__(self, sourceObject, targetObject, relation, functional = False):
        self.sourceObject = sourceObject
        self.targetObject = targetObject
        self.functional = functional
        self.relation = relation

    def compose(self, morphism)
