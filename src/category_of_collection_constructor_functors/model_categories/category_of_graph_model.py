from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism
import networkx as nx

class GraphModelCategory:

    """
    GraphModelCategory is a category with two objects and two non-identity morphism between them. The identity morphisms are modelled only conceptually.
    """

    def __init__(self, name, vertex_object_attributes = [], edge_object_attributes = [], objects = None, morphisms = None, converged_model_categories = []):
        self.name = name
        self.vertex_object_attributes = vertex_object_attributes
        self.edge_object_attributes = edge_object_attributes
        self.converged_model_categories = converged_model_categories
        if objects == None and morphisms == None:
            self.vertex_object = AbstractObject("vertexObject", "graph", self.vertex_object_attributes)
            self.edge_object = AbstractObject("edgeObject", "graph", self.edge_object_attributes)
            self.source_morphism = AbstractMorphism("sourceMorphism", self.edge_object, self.vertex_object)
            self.target_morphism = AbstractMorphism("targetMorphism", self.edge_object, self.vertex_object)
            self.objects = [self.vertex_object, self.edge_object]
            self.morphisms = [self.source_morphism, self.target_morphism]
        elif objects != None and morphisms != None:
            self.objects = objects
            self.morphisms = morphisms
        else:
            raise AttributeError("Wrong combination of attributes in the graph model category initialization.")

    def get_name(self):
        return self.name

    def get_model(self):
        return "graph"

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def get_attributes(self):
        return {"vertices": self.vertex_object_attributes, "edges": self.edge_object_attributes}

    def get_converged_model_categories(self):
        return self.converged_model_categories

    def add_converged_model_categories(self, new):
        self.converged_model_categories.append(new)

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
        try: 
            if type(self.edge_object) == list and type(self.vertex_object) == list:
                return ",".join(self.edge_object) + " -- source and target morphisms --> " + ", ".join(self.vertex_object)
            else:
                return "edge object -- source and target morphisms --> vertex object"
        except:
            result = ""
            for obj in self.objects:
                result = result + str(obj)
            return result