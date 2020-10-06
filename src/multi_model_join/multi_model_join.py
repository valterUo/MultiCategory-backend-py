from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship
from multi_model_join.graph_join_table import graph_join_table
from multi_model_join.table_join_table import table_join_table
from multi_model_join.graph_join_graph import graph_join_graph
from multi_model_join.table_join_graph import table_join_graph
from multi_model_join.table_join_tree import table_join_tree
from multi_model_join.graph_join_tree import graph_join_tree
from multi_model_join.tree_join_graph import tree_join_graph
from multi_model_join.tree_join_table import tree_join_table
from multi_model_join.tree_join_tree import tree_join_tree

""" Morphisms between collection constructors are not automatically evaluated. They model relationships between different models.
Because relationships generally are modelled as relations, this means that there is some amount of elements in the first collection
that are in a relation with some elements in the second collection. As border cases it is possible that there is no element in the
first collection that is in a relationship with any element in the second collection. On the other hand, the relationship does not need
to be functional. Multi-model join means that we take pairs (a, b) in the relation and create a new element combining a and b and substitute
it to the structure of a. The multi-model join works naturally in the sense that if a is not in relation with any b then a is not included
in the result.

It would be possible to create two morphisms from joined collections to the result collection. This needs to be implemented later.

Every join is implemented with two different parameters: INNER and OUTER. The difference is here the same as we have with relational
joins: outer join includes the first collection wholly even if there is no any element related to that and inner excludes such elements.

Multi-model join is considered as a first_collection -- collection_constructor_morphism --> second_collection that
factorizes through the join result so that first_collection --> join_result <-- second_collection. (This needs more studying.)
"""

class MultiModelJoin:

    def __init__(self, first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left = False, right = False, second_description = None, tree_attributes = None):
        self.first_collection_constructor = first_collection_constructor
        self.collection_constructor_morphism = collection_constructor_morphism
        self.second_collection_constructor = second_collection_constructor
        self.left = left
        self.right = right
        self.second_description = second_description
        self.tree_attributes = tree_attributes
        self.result, self.model_category_join = self.join()
        self.name = self.result.get_name()

        ## Projective legs from the result, the correct collection relationships needs to be implemented still
        left_leg_model_relationship = self.model_category_join.get_left_leg_model_relationship()
        left_leg_name = self.result.get_name() + "_to_" + self.first_collection_constructor.get_name()
        left_leg_collection_relationship = CollectionRelationship(left_leg_name, self.result.get_collection(), lambda x : x, self.first_collection_constructor.get_collection())
        self.left_leg = CollectionConstructorMorphism(left_leg_name, self.first_collection_constructor, left_leg_model_relationship, left_leg_collection_relationship, self.result)
        
        right_leg_model_relationship = self.model_category_join.get_right_leg_model_relationship()
        right_leg_name = self.result.get_name() + "_to_" + self.second_collection_constructor.get_name()
        right_leg_collection_relationship = CollectionRelationship(right_leg_name, self.result.get_collection(), lambda x : x, self.second_collection_constructor.get_collection())
        self.right_leg = CollectionConstructorMorphism(right_leg_name, self.second_collection_constructor, right_leg_model_relationship, right_leg_collection_relationship, self.result)

    def join(self):
        first_collection = self.first_collection_constructor.get_collection()
        second_collection = self.second_collection_constructor.get_collection()
        if type(first_collection) == TableCollection:
            if type(second_collection) == TableCollection:
                return table_join_table(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left)
            elif type(second_collection) == GraphCollection:
                return table_join_graph(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.second_description, self.left)
            elif type(second_collection) == TreeCollection:
                return table_join_tree(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.second_description, self.left)
        elif type(first_collection) == GraphCollection:
            if type(second_collection) == TableCollection:
                return graph_join_table(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left)
            elif type(second_collection) == GraphCollection:
                return graph_join_graph(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left, self.right)
            elif type(second_collection) == TreeCollection:
                return graph_join_tree(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left)
        elif type(first_collection) == TreeCollection:
            if type(second_collection) == TableCollection:
                return tree_join_table(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left, self.tree_attributes)
            elif type(second_collection) == GraphCollection:
                return tree_join_graph(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left, self.tree_attributes)
            elif type(second_collection) == TreeCollection:
                return tree_join_tree(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left, self.tree_attributes)

    def get_result(self):
        return self.result

    def get_name(self):
        return self.name

    def get_model(self):
        return self.result.get_model()

    def get_model_category_join(self):
        return self.model_category_join

    def get_left_leg(self):
        return self.left_leg

    def get_right_leg(self):
        return self.right_leg