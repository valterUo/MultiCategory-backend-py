from category_of_collection_constructor_functors.collection_constructor_error import CollectionConstructorMorphismCompositionError
class CollectionConstructorMorphism:

    """
    This class implements a morphisms between functors. This morphism is not natural transformation because functors do not need to be between the same categories.
    These morphisms can be considered as depedencies or relationships between datasets: for example functional dependencies, different kinds of queries, edges of a graph etc. can be
    modelled as instances of this class.
    Creating an instance of this class usually creates a new collection that is a result to the given relationship or query.
    """

    def __init__(self, name, domain_collection_constructor_functor, model_relationship, collection_relationship, target_collection_constructor_functor):
        self.name = name
        self.domain_collection_constructor_functor = domain_collection_constructor_functor
        self.target_collection_constructor_functor = target_collection_constructor_functor
        self.model_relationship = model_relationship
        self.collection_relationship = collection_relationship

    def get_name(self):
        return self.name

    def get_domain_collection_constructor_functor(self):
        return self.domain_collection_constructor_functor

    def get_target_collection_constructor_functor(self):
        return self.target_collection_constructor_functor

    def get_model_relationship(self):
        return self.model_relationship

    def get_collection_relationship(self):
        return self.collection_relationship

    ## Composition operation: compose(self, m) = self o m = self(m(-))
    ## If the domain and the target morphisms do no match, then the error is raised

    def compose(self, another_morphism):
        if another_morphism.get_target_collection_constructor_functor() == self.domain_collection_constructor_functor:
            composition1 = self.model_relationship.compose(another_morphism.get_model_relationship())
            composition2 = self.collection_relationship.compose(another_morphism.get_collection_relationship())
            return CollectionConstructorMorphism(another_morphism.get_domain_collection_constructor_functor(), composition1, composition2, self.target_collection_constructor_functor)
        else:
            raise CollectionConstructorMorphismCompositionError("Composition is not defined. Domain and target objects do not match.", "Composition is not defined.")