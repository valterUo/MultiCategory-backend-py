from category_of_collection_constructor_functors.model_categories.model_category_error import ModelRelationshipCompositionError
from supportive_functions.compositions import compose_list_of_dictionaries

class ModelRelationship:

    """
    We assume that relationship is given as a list of dictionaries which simply models mathematical relation between source and target.
    """

    def __init__(self, name, source_model, relationship, target_model):
        self.name = name
        self.source_model = source_model
        self.target_model = target_model
        self.relationship = relationship

    def get_name(self):
        return self.name
    
    def get_source_model(self):
        return self.source_model

    def get_target_model(self):
        return self.target_model

    def get_relationship(self):
        return self.relationship

    ## Composition operation: compose(self, m) = self o m = self(m(-))
    ## If the domain and the target do no match, then the error is raised

    def compose(self, another_model_relationship):
        if self.source_model == another_model_relationship.get_target_model():
            if type(self.relationship) == dict() and type(another_model_relationship.get_relationship()) == dict():
                new_relationship = compose_list_of_dictionaries(self.relationship, another_model_relationship.get_relationship())
            return ModelRelationship(self.name + " o " + another_model_relationship.get_name, another_model_relationship.get_source_model(), new_relationship, self.target_model)
        else:
            raise ModelRelationshipCompositionError("Composition is not defined.", "Composition is not defined.")