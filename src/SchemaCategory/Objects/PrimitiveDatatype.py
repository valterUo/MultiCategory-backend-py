from SchemaCategory.Morphisms.Morphism import Morphism

class PrimitiveDatatype:
    """Primitive datatype models those objects that are atomic. 
    
    They are always target objects for Nested datatypes and they cannot have outgoing morphisms i.e. they are never domain for any morphism. 
    """

    def __init__(self, name : str, typeVar : str, inComingMorphisms : [Morphism]):
        self.name = name
        self.typeVar = typeVar
        self.inComingMorphisms = inComingMorphisms
    
    def __eq__(self, other):
        return self.typeVar == other.typeVar