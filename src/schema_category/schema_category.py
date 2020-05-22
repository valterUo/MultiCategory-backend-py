from SchemaCategory.Morphisms.Morphism import Morphism

class SchemaCategory:

    def __init__(self, objects, morphisms):
        self.objects = objects
        self.morphisms = morphisms
    
    def __str__(self):
        allmorphisms = ""
        for morphism in self.morphisms:
            allmorphisms += str(morphism) + "\n"
        return allmorphisms

    def addMorphism(self, morphism):
            self.objects.add(morphism.sourceObject)
            self.objects.add(morphism.targetObject)
            self.morphisms.add(morphism)

    def addObject(self, obj):
        self.objects.add(obj)

    def containsObject(self, obj):
        return self.objects.contains(obj)
                