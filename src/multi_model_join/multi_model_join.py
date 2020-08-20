from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_join.model_category_join import join as model_join
import numpy
import os
from tables import *
import networkx as nx
from supportive_functions.row_manipulations import row_to_dictionary
from supportive_functions.compositions import merge_two_dicts
import pickle
from multi_model_join.graph_join_table import graph_join_table
from multi_model_join.table_join_table import table_join_table
from multi_model_join.graph_join_graph import graph_join_graph
from multi_model_join.table_join_graph import table_join_graph

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

    def __init__(self, first_collection_constructor, collection_constructor_morphism, second_collection_constructor, left = False, right = False, second_description = None):
        self.first_collection_constructor = first_collection_constructor
        self.collection_constructor_morphism = collection_constructor_morphism
        self.second_collection_constructor = second_collection_constructor
        self.left = left
        self.right = right
        self.second_description = second_description
        self.result = self.join()

    def join(self):
        first_collection = self.first_collection_constructor.get_collection()
        second_collection = self.second_collection_constructor.get_collection()

        if type(first_collection) == TableCollection:
            if type(second_collection) == TableCollection:
                result = table_join_table(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left)
            elif type(second_collection) == GraphCollection:
                result = table_join_graph(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.second_description)
            elif type(second_collection) == TreeCollection:
                #result = table_join_tree(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor)
                result = None
        elif type(first_collection) == GraphCollection:
            if type(second_collection) == TableCollection:
                result = graph_join_table(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left)
            elif type(second_collection) == GraphCollection:
                result = graph_join_graph(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor, self.left, self.right)
            elif type(second_collection) == TreeCollection:
                #esult = graph_join_tree(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor)
                result = None
        elif type(first_collection) == TreeCollection:
            if type(second_collection) == TableCollection:
                #result = tree_join_table(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor)
                result = None
            elif type(second_collection) == GraphCollection:
                #result = tree_join_graph(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor)
                result = None
            elif type(second_collection) == TreeCollection:
                #result = tree_join_tree(self.first_collection_constructor, self.collection_constructor_morphism, self.second_collection_constructor)
                result = None
        return result

    def get_result(self):
        return self.result