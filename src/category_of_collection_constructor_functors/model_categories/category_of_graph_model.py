from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism

class GraphModelCategory:

    """
    GraphModelCategory is a category with two objects and two non-identity morphism between them. The identity morphisms are modelled only conceptually.
    """

    def __init__(self, name, vertex_object = None, vertex_schema = None, edge_object = None, edge_schema = None, source_morphism = None, target_morphism = None):
        self.name = name
        self.vertex_schema = vertex_schema
        self.edge_schema = edge_schema
        if vertex_object == None and edge_object == None and source_morphism == None and target_morphism == None:
            self.vertex_object = AbstractObject("vertex_object")
            self.edge_object = AbstractObject("edge_object")
            self.source_morphism = AbstractMorphism("source_morphism", self.edge_object, self.vertex_object)
            self.target_morphism = AbstractMorphism("target_morphism", self.edge_object, self.vertex_object)
        else:
            self.edge_object = edge_object
            self.vertex_object = vertex_object
            self.source_morphism = source_morphism
            self.target_morphism = target_morphism

    def get_name(self):
        return self.name
    
    def get_edge_object(self):
        return self.edge_object

    def get_vertex_object(self):
        return self.vertex_object

    def get_vertex_schema(self):
        return self.vertex_schema

    def get_edge_schema(self):
        return self.edge_schema

    def __str__(self):
        return "edge -- source and target morphisms --> vertex"