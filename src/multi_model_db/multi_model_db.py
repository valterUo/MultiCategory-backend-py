from multi_model_db.multi_model_db_instance_category.instance_category import InstanceCategory
from multi_model_db.multi_model_db_schema_category.schema_category import SchemaCategory

"""
This class models the functor category that consists of objects (collection constructor functors) and morphisms (functors between those functors).
From the objects and morphisms we can automatically extract two categories: Schema category and instance category.

Schema category consists of model categories and relations between them.
Instance category consists of data model instances and relations between them.

Schema category is functorially mapped to the instance category and this mapping is defined with collection constructors functors on objects and information how morphisms are
mapped is coded into the class.
"""

class MultiModelDB:

    def __init__(self, name, objects, morphisms, available = False, schema_category = None, instance_category = None):
        self.name = name
        self.objects = objects
        self.morphisms = morphisms
        self.available = available
        self.schema_category = schema_category
        self.instance_category = instance_category
        if self.schema_category == None:
            self.schema_category = self.construct_schema_category()
        if self.instance_category == None:
            self.instance_category = self.construct_instance_category()
        
            
    def construct_schema_category(self):
        objects = dict()
        morphisms = dict()
        for obj in self.objects:
            objects[obj] = self.objects[obj].get_model_category()
        for mor in self.morphisms:
            morphisms[mor] = self.morphisms[mor].get_model_relationship()
        return SchemaCategory(self.name + " schema category", objects, morphisms)

    def construct_instance_category(self):
        objects = dict()
        morphisms = dict()
        for obj in self.objects:
            objects[obj] = self.objects[obj].get_collection()
        for mor in self.morphisms:
            morphisms[mor] = self.morphisms[mor].get_collection_relationship()
        return InstanceCategory(self.name + " instance category", objects, morphisms)

    def get_name(self):
        return self.name

    def get_objects(self):
        return self.objects

    def get_morphisms(self):
        return self.morphisms

    def is_available(self):
        return self.available

    def add_object(self, new_object):
        self.schema_category.add_object(new_object.get_model_category())
        self.instance_category.add_object(new_object.get_collection())
        self.objects[new_object.get_name()] = new_object

    def add_morphism(self, new_morphism):
        self.schema_category.add_morphism(new_morphism.get_model_relationship())
        self.instance_category.add_morphism(new_morphism.get_collection_relationship())
        self.morphisms[new_morphism.get_name()] = new_morphism

    def get_instance_category(self):
        return self.instance_category

    def get_schema_category(self):
        return self.schema_category

    def get_schema_category_nx_graph(self):
        return self.schema_category.get_nx_graph()

    def get_instance_category_nx_graph(self):
        return self.instance_category.get_nx_graph()

    def get_str_list_of_objects(self):
        result = []
        for key in self.objects:
            result.append({ 'label': self.objects[key].get_name(), 'value': key })
        return result

    def get_morphisms_for_pair_of_objects(self, obj1, obj2):
        result = []
        for mor_key in self.morphisms:
            mor = self.morphisms[mor_key]
            morphism_domain_name = mor.get_domain_collection_constructor_functor().get_name()
            morphism_target_name = mor.get_target_collection_constructor_functor().get_name()
            if morphism_domain_name == obj1 and morphism_target_name == obj2:
                result.append({'label': mor.get_name(), 'value': mor_key})
        return result
            

    def __str__(self):
        return self.name