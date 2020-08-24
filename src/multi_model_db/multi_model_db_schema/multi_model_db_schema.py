import networkx as nx

""" 
If multi-model database is considered to be a category of collection constructor functors and morphisms between them, then schema category
consists of objects that are the domain categories of the collection constructor functors and morphisms are the abstract arrows pointing from
the domain object to the target object.
"""

class MultiModelDBSchema:

    def __init__(self, objects, morphisms):
        self.objects = objects
        self.morphisms = morphisms

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def get_nx_graph(self):
        return None