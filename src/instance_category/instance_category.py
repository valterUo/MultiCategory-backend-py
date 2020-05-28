class InstanceCategory:

    def __init__(self, name, objects, morphisms):
        self.name = name
        self.objects = objects
        self.morphisms = morphisms

    def get_name(self):
        return self.name

    def get_objects(self):
        return self.objects
    
    def get_morphisms(self):
        return self.morphisms