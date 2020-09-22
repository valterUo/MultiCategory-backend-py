import networkx as nx

""" 
If multi-model database is considered to be a category of collection constructor functors and morphisms between them, then schema category
consists of objects that are the domain categories of the collection constructor functors and morphisms are the abstract arrows pointing from
the domain object to the target object.
"""

class SchemaCategory:

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

    def add_object(self, new_object):
        self.objects[new_object.get_name()] = new_object

    def add_morphism(self, new_morphism):
        self.morphisms[new_morphism.get_name()] = new_morphism

    def get_nx_graph(self):
        G = nx.DiGraph(title = self.name)
        node_list, edge_list = [], [] 
        for obj in self.objects.values():
            node_list.append((obj.get_name(), {"label": obj.get_name()}))
        G.add_nodes_from(node_list)
        for morphism in self.morphisms.values():
            edge_list.append((morphism.get_source_model().get_name(), morphism.get_target_model().get_name(), { "label": morphism.get_name() }))
        G.add_edges_from(edge_list)
        return G