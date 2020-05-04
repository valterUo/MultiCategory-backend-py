from SchemaCategory.Objects.PrimitiveDatatype import PrimitiveDatatype
from SchemaCategory.Objects.NestedDatatype import NestedDatatype
from SchemaCategory.Morphisms.Morphism import Morphism


class InstanceFunctor:
    """
    Instance functor is a mapping from the Instance category to Schema category. The idea is that is describes the current state of the database. 
    It is sort of data forgetting function in the sense that it forgets the concrete data when it maps from Instance to Schema.

    CollectionObject other than set and no target objects -> PrimitiveDatatype 
    CollectionObject set and target objects -> NestedDatatype 
    Morphism -> Morphism
    """

    def __init__(self, instanceCategory, schemaCategory = None):
        self.instanceCategory = instanceCategory
        if schemaCategory == None:
            self.schemaCategory = constructSchemaCategory(instanceCategory)
        else:
            self.schemaCategory = schemaCategory
    

    def constructSchemaCategory(self):
        for mor in self.instanceCategory:
            target = NestedDatatype(mor.targetObject.name, mor.targetObject.collectionType, [], [])
            if no_outgoing_morphisms(mor.targetObject):
                target = PrimitiveDatatype(mor.targetObject.name, mor.targetObject.collectionType, [])
            nestedTypeSource = NestedDatatype(mor.sourceObject.name, mor.sourceObject.collectionType, [], [])
            newMorphism = Morphism(mor.name, nestedTypeSource, target)
            self.schemaCategory.addMorphism(newMorphism)


    def no_outgoing_morphisms(self, collectionObject):
        for m in self.instanceCategory.morphisms:
            if m.sourceObject == collectionObject:
                return False
        return True