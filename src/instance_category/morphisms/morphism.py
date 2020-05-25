import functools
from instance_category.objects.collection_object import CollectionObject


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

    The relation can be inputted as a function or as an instance of BinRelation which is slithy generalized 
    """

    def __init__(self, name, sourceObject, relation, targetObject, functional=False):
        self.name = name
        self.sourceObject = sourceObject
        self.targetObject = targetObject
        self.functional = functional
        self.relation = relation
        if targetObject.getCollection() == None:
            collection = []
            for elem in sourceObject.get_access_to_iterable(sourceObject.getCollection()):
                collection.append(relation(elem))
            self.targetObject.setCollection(collection)

    def compose(self, morphism):
        if morphism.targetObject == self.sourceObject:
            newLambda = None
            if self.functional and morphism.functional:
                # Both morphisms can be expressed as functions and thus we have the ordinary function composition.
                newLambda = morphism.relation(self.relation)
                isFunctional = True
            elif self.functional:
                # Morphism.relation is ''set valued'' function i.e relation. In this case we take each element corresponding the image of x and map those elements using the function self.relation.
                def newLambda(x): return map(
                    self.relation, morphism.relation(x))
                isFunctional = False
            elif morphism.functional:
                # The same as the previous case except that the roles of morphism.relation and self.relation have changed. After all, this composition works as a function composition.
                newLambda = morphism.relation(self.relation)
                isFunctional = False
            else:
                # Both are non-functional relations i.e. we can think that values are mapped to sets.
                def helper(y, x):
                    z = y.union(self.relation(x))
                    return z
                def newLambda(x):
                    return functools.reduce(helper, morphism.relation(x), set())
                isFunctional = False
            return Morphism(morphism.name + " o " + self.name, self.sourceObject, morphism.targetObject, newLambda, isFunctional)

    def getRelation(self, variable):
        return self.relation(variable)

    def getFunctional(self):
        return self.functional