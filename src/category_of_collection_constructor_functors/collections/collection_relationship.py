from category_of_collection_constructor_functors.collections.collection_errors import CollectionRelationshipCompositionError
from supportive_functions.compositions import compose_lambda_functions

class CollectionRelationship:

    def __init__(self, name, source_collection, relationship, target_collection):
        self.name = name
        self.source_collection = source_collection
        self.target_collection = target_collection
        self.relationship = relationship

    def get_name(self):
        return self.name

    def get_source_collection(self):
        return self.source_collection

    def get_target_collection(self):
        return self.target_collection

    def get_relationship(self, value):
        return self.relationship(value)

    ## Composition operation: compose_relationships(self, m) = self o m = self(m(-))
    ## If the domain and the target do no match, then the error is raised

    def compose(self, another_collection_relationship):
        if self.source_collection == another_collection_relationship.get_target_collection():
            new_lambda_function = compose_lambda_functions(self.relationship, another_collection_relationship.get_relationship())
            return CollectionRelationship(self.name + " o " + another_collection_relationship.get_name(), another_collection_relationship.get_source_collection(), new_lambda_function, self.target_collection)
        else:
            raise CollectionRelationshipCompositionError("Composition is not defined.", "Composition is not defined.")