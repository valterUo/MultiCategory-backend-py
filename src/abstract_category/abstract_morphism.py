from abstract_category.composition_error import CompositionError

class AbstractMorphism:

    def __init__(self, name, source, target):
        self.name = name
        self.source = source
        self.target = target

    def get_name(self):
        return self.name

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def compose(self, morphism):
        if morphism.get_target() == self.source:
            return AbstractMorphism(self.name + " o " + morphism.get_name(), morphism.get_source(), self.target)
        else:
            raise CompositionError("Composition is not defined.", "Composition is not defined.")