from abstract_category.abstract_object import AbstractObject
import networkx as nx

class GenericModelCategory:

    def __init__(self, name, objects, morphisms, models):
        self.name = name
        self.objects = objects
        self.morphisms = morphisms
        self.models = models

    def get_name(self):
        return self.name

    def get_models(self):
        return self.models

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def get_attributes(self):
        return []

    def get_nx_graph(self):
        G, edges, nodes = nx.DiGraph(), [], []
        for mor in self.morphisms:
            edges.append((mor.get_source().get_id(), mor.get_target().get_id(), {'label': mor.get_name()}))
        G.add_edges_from(edges)
        for obj in self.objects:
            nodes.append((obj.get_id(), {'label': obj.get_name()}))
        G.add_nodes_from(nodes)
        return G

    def __str__(self):
        return "Objects: " + str(self.objects) + " Morphisms: " + str(self.morphisms)