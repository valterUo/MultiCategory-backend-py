from schema_category.morphisms.morphism import Morphism as schema_category_morphism
from instance_category.morphisms.morphism import Morphism as instance_category_morphism
from schema_category.objects.datatype_object import DatatypeObject
from schema_category.schema_category import SchemaCategory
from instance_category.objects.collection_object import CollectionObject
from instance_functor.instance_functor_error import MorphismNotInInstanceDomain, ObjectNotInInstanceDomain, KeyNotInInstanceDomain, InstanceFunctorError


class InstanceFunctor:
    """
    Instance functor is a mapping from the Instance category to Schema category. The idea is that is describes the current state of the database. 
    It is sort of data forgetting function in the sense that it forgets the concrete data when it maps from Instance to Schema.
    """

    def __init__(self, instance_category, schema_category=None):
        self.instance_category = instance_category
        if schema_category == None:
            self.schema_category = self.construct_schema_category(
                instance_category)
        else:
            self.schema_category = schema_category

    def get_schema_category(self):
        return self.schema_category

    def get_instance_category(self):
        return self.instance_category

    def construct_schema_category(self, instance_category):
        objects = instance_category.get_objects()
        morphisms = instance_category.get_morphisms()
        schema_objects, schema_morphisms = dict(), dict()
        for morphism in morphisms:
            instance_morphism = morphisms[morphism]
            source = instance_morphism.get_source_object()
            target = instance_morphism.get_target_object()
            if source.getName() not in schema_objects:
                source_schema_object = self.construct_collection_object(source)
                schema_objects[source.getName()] = source_schema_object
            if target.getName() not in schema_objects:
                target_schema_object = self.construct_collection_object(target)
                schema_objects[target.getName()] = target_schema_object
            schema_morphism = schema_category_morphism(instance_morphism.get_name(
            ), schema_objects[source.getName()], schema_objects[target.getName()])
            schema_morphisms[morphism] = schema_morphism
            source_schema_object.add_outgoing_morphism(schema_morphism)
            target_schema_object.add_incoming_morphism(schema_morphism)
        return SchemaCategory(instance_category.get_name(), schema_objects, schema_morphisms)

    def construct_collection_object(self, collection_object):
        schema_object = DatatypeObject(
            collection_object.getName(), collection_object.getCollectionType())
        return schema_object

    def instance_map(self, object_or_morphism):
        instance_objects = self.instance_category.get_objects()
        instance_morphisms = self.instance_category.get_morphisms()
        schema_objects = self.schema_category.get_objects()
        schema_morphisms = self.schema_category.get_morphisms()

        if type(object_or_morphism) == CollectionObject:
            for obj_key in instance_objects:
                if instance_objects[obj_key] == object_or_morphism:
                    return schema_objects[obj_key]
            else:
                raise ObjectNotInInstanceDomain(
                    object_or_morphism, "The object not in the objects of the instance category.")
        elif type(object_or_morphism) == instance_category_morphism:
            for morph_key in instance_morphisms:
                if instance_morphisms[morph_key] == object_or_morphism:
                    return schema_morphisms[morph_key]
            else:
                raise MorphismNotInInstanceDomain(
                    object_or_morphism, "The morphism not in the morphisms of the instance category.")
        elif type(object_or_morphism) == str:
            if object_or_morphism in instance_objects.keys():
                return schema_objects[object_or_morphism]
            elif object_or_morphism in instance_morphisms.keys():
                return schema_morphisms[object_or_morphism]
            else:
                raise KeyNotInInstanceDomain(
                    object_or_morphism, "The key does not point to any element in the instance category.")
        else:
            raise InstanceFunctorError(
                object_or_morphism, "The type of the input is wrong.")