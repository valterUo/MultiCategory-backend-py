from abstract_category.composition_error import CompositionError
import uuid

class AbstractMorphism:

    def __init__(self, name, source, target, model):
        self.id = uuid.uuid4()
        self.name = name
        self.source = source
        self.target = target
        self.model = model

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_model(self):
        return self.model

    def compose(self, morphism):
        if morphism.get_target() == self.source:
            return AbstractMorphism(self.name + " o " + morphism.get_name(), morphism.get_source(), self.target)
        else:
            raise CompositionError("Composition is not defined.", "Composition is not defined.")