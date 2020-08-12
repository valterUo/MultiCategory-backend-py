from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism

class GraphModelCategory:

    """
    GraphModelCategory is a category with two objects and two non-identity morphism between them. The identity morphisms are modelled only conceptually.
    """

    def __init__(self, name, vertex_object = None, edge_object = None, source_morphism = None, target_morphism = None):
        self.name = name
        self.edge_object = edge_object
        self.vertex_object = vertex_object
        self.source_morphism = source_morphism
        self.target_morphism = target_morphism

        if vertex_object == None:
            self.vertex_object = AbstractObject("vertex_object")
        if edge_object == None:
            self.edge_object = AbstractObject("edge_object")
        if source_morphism == None:
            self.source_morphism = AbstractMorphism("source_morphism", self.edge_object, self.vertex_object)
        if target_morphism == None:
            self.target_morphism = AbstractMorphism("target_morphism", self.edge_object, self.vertex_object)

    def get_name(self):
        return self.name
    
    def get_edge_object(self):
        return self.edge_object

    def get_vertex_object(self):
        return self.vertex_object

    def get_objects(self):
        return [self.vertex_object, self.edge_object]

    def __str__(self):
        if type(self.edge_object) == list and type(self.vertex_object) == list:
            return ",".join(self.edge_object) + " -- source and target morphisms --> " + ", ".join(self.vertex_object)
        else:
            return "edge object -- source and target morphisms --> vertex object"