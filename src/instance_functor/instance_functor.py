from schema_category.objects.nested_datatype import NestedDatatype
from schema_category.morphisms.morphism import Morphism


class InstanceFunctor:
    """
    Instance functor is a mapping from the Instance category to Schema category. The idea is that is describes the current state of the database. 
    It is sort of data forgetting function in the sense that it forgets the concrete data when it maps from Instance to Schema.

    CollectionObject other than set and no target objects -> PrimitiveDatatype 
    CollectionObject set and target objects -> NestedDatatype 
    Morphism -> Morphism
    """

    def __init__(self, instanceCategory, schemaCategory=None):
        self.instanceCategory = instanceCategory
        if schemaCategory == None:
            self.schemaCategory = constructSchemaCategory(instanceCategory)
        else:
            self.schemaCategory = schemaCategory


    def constructSchemaCategory(self):
        return None