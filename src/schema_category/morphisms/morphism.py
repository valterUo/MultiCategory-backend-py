from schema_category.morphisms.composition_error import CompositionError

class Morphism:
    
    def __init__(self, name, source_object, target_object):
        self.name = name
        self.source_object = source_object
        self.target_object = target_object

    def __str__(self):
        return str(self.source_object) + " -- " + self.name + " --> " + str(self.target_object)
    
    def compose(self, other):
        if self.target_object == other.source_object:
            return Morphism(self.source_object, other.target_object)
        else: 
            raise CompositionError(self, "Not composable morphisms.")

    def get_source_object(self):
        return self.source_object

    def get_target_object(self):
        return self.target_object