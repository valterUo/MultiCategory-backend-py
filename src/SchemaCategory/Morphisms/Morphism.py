from SchemaCategory.Morphisms.CompositionError import CompositionError

class Morphism:
    
    def __init__(self, sourceObj, targetObj):
        self.sourceObj = sourceObj
        self.targetObj = targetObj
    
    def compose(self, other):
        if self.targetObj == other.sourceObj:
            return Morphism(self.sourceObj, other.targetObj)
        else: 
            raise CompositionError(self, "Not composable morphisms.")