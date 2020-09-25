from abstract_category.abstract_object import AbstractObject
import networkx as nx

class TableModelCategory:

    """
    TableModelCategory is a discrete category with as many objects as there are attributes in the table.
    We can assume that objects have some ordering. 
    The sequence of attributes is always required. 
    The identity morphisms are modelled only conceptually.
    """

    def __init__(self, name, attributes = [], primary_keys = None, objects = None, morphisms = None, converged_model_categories = []):
        self.name = name
        self.primary_keys = primary_keys
        self.objects = []
        self.attributes = attributes
        self.converged_model_categories = converged_model_categories
        if morphisms == None:
            self.morphisms = []
        else:
            self.morphisms = morphisms
        if objects == None:
            self.objects.append(AbstractObject(self.name, "relational", attributes))
        else:
            self.objects = objects

    def get_name(self):
        return self.name

    def get_model(self):
        return "relational"
    
    def get_attributes(self):
        attributes = []
        for obj in self.objects:
            attributes.append(obj.get_value()[0])
        return attributes

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def get_primary_keys(self):
        return self.primary_keys

    def get_attributes(self):
        return self.attributes
    
    def get_converged_model_categories(self):
        return self.converged_model_categories

    def add_converged_model_categories(self, new):
        self.converged_model_categories.append(new)

    def get_nx_graph(self):
        if self.converged_model_categories == []:
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