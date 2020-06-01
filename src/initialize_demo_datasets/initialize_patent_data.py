import os
dirname = os.path.dirname(__file__)
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from instance_category.instance_category import InstanceCategory

def init():
    objects = dict()
    morphisms = dict()