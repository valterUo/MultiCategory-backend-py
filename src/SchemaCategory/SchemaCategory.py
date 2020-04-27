from SchemaCategory.Morphisms.Morphism import Morphism

class SchemaCategory:

    def __init__(self, objects, morphisms : [Morphism]):
        self.objects = objects
        self.morphisms = morphisms
    
    # @classmethod
    # def fromfilename(cls, name):
    #     return cls(open(name, 'rb'))
    
    def __str__(self):
        allmorphisms = ""
        for morphism in self.morphisms:
            allmorphisms += str(morphism) + "\n"
        return allmorphisms