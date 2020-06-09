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

    The relation parameter can be defined as a function that takes an element from source_object and identifies some amount of objects from the target object.
    The relation is a subset of source object x target object where we consider source and target objects suitable as sets of elements from the collections
    which are stored in the objects.

    The composition function in this class needs to satisfy the compostion rule of relation: the composition of relations R : A -> B and S : B -> C is S o R where a(S o R)c
    if there exists such b in B that aSb and bRc.

    The relation can be inputted as a function or as an instance of BinRelation which is slithy generalized 
    """

    def __init__(self, name, source_object, relation, target_object, functional=False, constant = False):
        self.name = name
        self.source_object = source_object
        self.target_object = target_object
        self.functional = functional
        self.relation = relation
        self.constant = constant
        if target_object.get_collection() == None:
            collection = []
            if self.constant:
                collection.append(self.relation(None))
            else:
                for elem in source_object.get_access_to_iterable():
                    collection.append(self.relation(elem))
            self.target_object.set_collection(collection)

    def __eq__(self, other):
        return self.name == other.name #and self.get_source_object == other.source_object and self.target_object == other.target_object)

    def compose(self, morphism):
        if morphism.target_object == self.source_object:
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
            return Morphism(morphism.name + " o " + self.name, self.source_object, morphism.target_object, newLambda, isFunctional)

    def getRelation(self, variable):
        return self.relation(variable)

    def getFunctional(self):
        return self.functional

    def get_name(self):
        return self.name

    def get_source_object(self):
        return self.source_object

    def get_target_object(self):
        return self.target_object

    def get_source_object_name(self):
        return self.source_object.getName()

    def get_target_object_name(self):
        return self.target_object.getName()
