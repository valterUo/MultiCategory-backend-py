from instance_category.objects.collection_object import CollectionObject
from multi_model_join.relational_join import *
from multi_model_join.graph_join import *
from multi_model_join.xml_join import *
from multi_model_join.help_functions import *
import networkx as nx
import copy


def join(collectionObject1, morphism, collectionObject2, pattern=None):
    type1 = collectionObject1.getCollectionType()
    type2 = collectionObject2.getCollectionType()
    if type1 == "relational":
        if type2 == "relational":
            if morphism.getFunctional():
                return join_relational_relational_over_functional_morphism(collectionObject1, morphism, collectionObject2)
            else:
                return join_relational_relational_over_nonfunctional_morphism(collectionObject1, morphism, collectionObject2)
        elif type2 == "property graph":
            return None
    elif type1 == "property graph":
        if type2 == "property graph":
            if pattern == None:
                return "Error"
            return join_graph_graph(collectionObject1, morphism, collectionObject2)