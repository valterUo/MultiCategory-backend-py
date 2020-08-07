class MultiModelDBSchema:

    def __init__(self, objects, morphisms):
        self.objects = objects
        self.morphisms = morphisms

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def print_schema_category_as_graph(self):
        return None