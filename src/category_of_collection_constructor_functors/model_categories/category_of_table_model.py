from abstract_category.abstract_object import AbstractObject
import networkx as nx

class TableModelCategory:

    """
    TableModelCategory is a discrete category with as many objects as there are attributes in the table.
    We can assume that objects have some ordering. 
    The sequence of attributes is always required. 
    The identity morphisms are modelled only conceptually.
    """

    def __init__(self, name, attributes, primary_key = None):
        self.name = name
        self.attributes = attributes
        self.primary_key = primary_key
        self.objects = []
        self.morphisms = []
        for attribute in self.attributes:
            self.objects.append(AbstractObject(attribute, "relational"))

    def get_name(self):
        return self.name

    def get_model(self):
        return "relational"
    
    def get_attributes(self):
        return self.attributes

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def get_primary_key(self):
        return self.primary_key

    def get_nx_graph(self):
        G, edges, nodes = nx.DiGraph(), [], []
        for mor in self.morphisms:
            edges.append(mor.get_source().get_id(), mor.get_target().get_id(), {'label': mor.get_name()})
        G.add_edges_from(edges)
        for obj in self.objects:
            nodes.append((obj.get_id(), {'label': obj.get_name()}))
        G.add_nodes_from(nodes)
        return G

    def __str__(self):
        return ", ".join(self.attributes)