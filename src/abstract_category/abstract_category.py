class AbstractCategory:

    def __init__(self, objects, morphisms):
        self.objects = objects
        self.morphisms = morphisms
    
    def get_objects(self):
        return self.objects
    
    def get_morphisms(self):
        return self.morphisms