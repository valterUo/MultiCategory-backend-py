import networkx as nx

""" 
If multi-model database is considered to be a category of collection constructor functors and morphisms between them, then instance category
consists of objects that are the target collections of the collection constructor functors and morphisms are the abstract arrows pointing from
the domain object to the target object.

Objects belong to class CollectionConstructor which are identified by their names.
Morphisms belong to class CollectionConstructorMorphism which are indentified by their names.
"""

class MultiModelDBInstance:

    def __init__(self, name, objects, morphisms):
        self.name = name
        self.objects = objects
        self.morphisms = morphisms

    def get_name(self):
        return self.name

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def get_nx_graph(self):
        G = nx.DiGraph(title = self.name)
        node_list, edge_list = [], [] 
        for obj in self.objects.values():
            node_list.append((obj.get_name(), {"label": obj.get_name() + " " + obj.get_model()}))
        G.add_nodes_from(node_list)
        for morphism in self.morphisms.values():
            edge_list.append((morphism.get_domain_collection_constructor_functor().get_name(), morphism.get_target_collection_constructor_functor().get_name(), {"label": morphism.get_name()}))
        G.add_edges_from(edge_list)
        return G