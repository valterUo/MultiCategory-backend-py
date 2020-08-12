from multi_model_join.model_category_join import join as model_join

class MultiModelJoin:

    """
    Multi-model join is considered as a first_collection -- collection_constructor_morphism --> second_collection that
    factorizes through the join result so that first_collection --> join_result <-- second_collection. (This needs more studying.)
    """

    def __init__(self, first_collection, collection_constructor_morphism, second_collection, joining_pattern = None):
        self.first_collection = first_collection
        self.second_collection = second_collection
        self.collection_constructor_morphism = collection_constructor_morphism
        self.joining_pattern = joining_pattern

        ## Result
        self.join_result
        self.first_leg
        self.second_leg

    def join_models(self):
        model_join_result = model_join(self.first_collection.get_model_category(), self.collection_constructor_morphism.get_model_relationship(), self.second_collection.get_model_category())
        return model_join_result

    def join_collections(self):
        collection_join_result = None
        return collection_join_result