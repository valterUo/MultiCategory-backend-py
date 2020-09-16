from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism
import networkx as nx
import copy

class RootObject:
    
    def __init__(self, name):
        self.name = name

class TreeModelCategory:

    """
    TreeModelCategory is a category with two objects and a single non-identity morphism between them. The target object is a disjoint union of the domain object and a special
    element * that satisfies the idea that * is the parent of the root. This means that "preimage of *" is the unique root of the tree. 
    Tree is a data structure where each node has a unique parent node except the root. The single morphism models this relationship between the nodes.
    If a fixed collection of attributes is known for the nodes, then this attribute collection can be assigned to self.nodes variable.
    Moreover, if the tree structure is still more fixed, a certain function can be assined to self.parent_of variable.
    Note that the edges in the tree do not contain any information. The identity morphisms are modelled only conceptually.
    """

    def __init__(self, name, node_object_attributes = [], objects = None, morphisms = None):
        self.name = name
        if objects == None or morphisms == None:
            self.root = RootObject(name)
            self.nodes = AbstractObject("nodes", "tree", node_object_attributes)
            self.nodes_with_disjoint_root = AbstractObject("nodes + root", "tree", [node_object_attributes, self.root])
            self.morphism = AbstractMorphism("parent_of", self.nodes, self.nodes_with_disjoint_root)
            self.morphisms = [self.morphism]
            self.objects = [self.nodes, self.nodes_with_disjoint_root]
        elif objects != None and morphisms != None:
            self.objects = objects
        else:
            raise AttributeError("Wrong combination of attributes in the tree model category initialization.")

    def get_name(self):
        return self.name

    def get_model(self):
        return "tree"
    
    def get_nodes(self):
        return self.nodes

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

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
        return "nodes -- parent_of --> nodes + root"