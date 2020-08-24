from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism
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

    def __init__(self, name, nodes = None, parent_of = None):
        self.name = name
        self.nodes = nodes
        self.root = RootObject(name)
        self.parent_of = parent_of
        if nodes != None:
            self.nodes_with_disjoint_root = copy.deepcopy(nodes).append(self.root)
        
        if nodes == None:
            self.nodes = AbstractObject("nodes")
            self.nodes_with_disjoint_root = [self.nodes, self.root]
        if parent_of == None:
            self.parent_of = AbstractMorphism("parent_of", self.nodes, self.nodes_with_disjoint_root)

    def get_name(self):
        return self.name

    def get_model(self):
        return "tree"
    
    def get_nodes(self):
        return self.nodes

    def get_objects(self):
        return [self.nodes]

    def __str__(self):
        return "nodes -- parent_of --> nodes + {*}"