from SchemaCategory.Morphisms.Morphism import Morphism

class SchemaCategory:

    def __init__(self, objects, morphisms : [Morphism]):
        self.objects = objects
        self.morphisms = morphisms
    