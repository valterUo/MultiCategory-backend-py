from SchemaCategory.Morphisms.Morphism import Morphism
from SchemaCategory.Objects.PrimitiveDatatype import PrimitiveDatatype

class NestedDatatype:
    """Nested datatype models those objects that are constructed from primitive datatypes or other nested datatypes. 
    
    They can serve as a domain or target object for a morphism. 
    """

    def __init__(self, name : str, inComingMorphisms : [Morphism], outGoingMorphisms : [Morphism]):
        self.name = name
        self.inComingMorphisms = inComingMorphisms
        self.outGoingMorphisms = outGoingMorphisms

    def __eq__(self, other):
        return self.name == other.name

    def add_morphism(self, morphism : Morphism):
        if self == morphism.sourceObj:
            self.outGoingMorphisms.append(morphism)
        elif self == morphism.targetObj:
            self.inComingMorphisms.append(morphism)