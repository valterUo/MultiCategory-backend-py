from schema_category.morphisms.morphism import Morphism
from schema_category.objects.datatype_object import DatatypeObject
from schema_category.schema_category import SchemaCategory


class InstanceFunctor:
    """
    Instance functor is a mapping from the Instance category to Schema category. The idea is that is describes the current state of the database. 
    It is sort of data forgetting function in the sense that it forgets the concrete data when it maps from Instance to Schema.

    CollectionObject other than set and no target objects -> PrimitiveDatatype 
    CollectionObject set and target objects -> NestedDatatype 
    Morphism -> Morphism
    """

    def __init__(self, instance_category, schema_category = None):
        self.instance_category = instance_category
        if schema_category == None:
            self.schema_category = self.construct_schema_category(instance_category)
        else:
            self.schema_category = schema_category


    def construct_schema_category(self, instance_category):
        objects = instance_category.get_objects()
        morphisms = instance_category.get_morphisms()
        schema_objects, schema_morphisms = dict(), dict()
        for morphism in morphisms:
            instance_morphism = morphisms[morphism]
            source = instance_morphism.get_source_object()
            target = instance_morphism.get_target_object()
            if source.getName() not in schema_objects:
                source_schema_object = self.parse_collection_object(source)
                schema_objects[source.getName()] = source_schema_object
            if target.getName() not in schema_objects:
                target_schema_object = self.parse_collection_object(target)
                schema_objects[target.getName()] = target_schema_object
            schema_morphism = Morphism(instance_morphism.get_name(), schema_objects[source.getName()], schema_objects[target.getName()])
            schema_morphisms[morphism] = schema_morphism
            source_schema_object.add_outgoing_morphism(schema_morphism)
            target_schema_object.add_incoming_morphism(schema_morphism)
        return SchemaCategory(instance_category.get_name(), schema_objects, schema_morphisms)


    def parse_collection_object(self, collection_object):
        schema_object = DatatypeObject(collection_object.getName(), collection_object.getCollectionType())
        return schema_object

    def get_schema_category(self):
        return self.schema_category

    def get_instance_category(self):
        return self.instance_category