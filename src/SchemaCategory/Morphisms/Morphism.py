from SchemaCategory.Morphisms.CompositionError import CompositionError

class Morphism:
    
    def __init__(self, name, sourceObj, targetObj):
        self.name = name
        self.sourceObj = sourceObj
        self.targetObj = targetObj

    def __str__(self):
        return "Name: " + self.name + ", source object: " + str(self.sourceObj) + ", target object: " + str(self.targetObj)
    
    def compose(self, other):
        if self.targetObj == other.sourceObj:
            return Morphism(self.sourceObj, other.targetObj)
        else: 
            raise CompositionError(self, "Not composable morphisms.")