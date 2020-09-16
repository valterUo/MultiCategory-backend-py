from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory
from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship

class ModelCategoryJoin:

    def __init__(self, first_model_category, model_relationship, second_model_category, left = False, right = False):
        self.first_model_category = first_model_category
        self.model_relationship = model_relationship
        self.second_model_category = second_model_category
        self.left = left
        self.right = right
        self.result, self.left_leg_model_relationship, self.right_leg_model_relationship = self.join()

    def get_result(self):
        return self.result

    def get_left_leg_model_relationship(self):
        return self.left_leg_model_relationship

    def get_right_leg_model_relationship(self):
        return self.right_leg_model_relationship

    def join(self):
        join_name = self.first_model_category.get_name() + " + " + self.second_model_category.get_name()
        join_objects = dict()

        model_rel = self.model_relationship.get_relationship()
        if type(model_rel) == list:
            for rel in model_rel:
                join_objects.update(self.create_objects_for_given_relation(rel))
        elif type(model_rel) == dict:
            join_objects.update(self.create_objects_for_given_relation(rel))

        join_morphisms = self.create_morphisms(join_objects)

        print(list(join_objects.values())[0].get_values())
        print(join_morphisms)

        if type(self.first_model_category) == TableModelCategory:
            result = TableModelCategory(join_name, objects = list(join_objects.values()), primary_key = self.first_model_category.get_primary_key())
        elif type(self.first_model_category) == GraphModelCategory:
            result = GraphModelCategory(join_name, objects = list(join_objects.values()), morphisms = join_morphisms)
        elif type(self.first_model_category) == TreeModelCategory:
            result = TreeModelCategory(join_name, objects = list(join_objects.values()), morphisms = join_morphisms)
        
        left_leg_model_relationship = ModelRelationship("Left projection from " + result.get_name() + " to " + self.first_model_category.get_name(), result, self.project_left_leg(self.model_relationship.get_relationship()), self.first_model_category)
        right_leg_model_relationship = ModelRelationship("Right projection from " + result.get_name() + " to " + self.second_model_category.get_name(), result, self.project_right_leg(self.model_relationship.get_relationship()), self.second_model_category)

        return result, left_leg_model_relationship, right_leg_model_relationship

    def create_objects_for_given_relation(self, rel):
        join_objects = dict()
        for first_object in self.first_model_category.get_objects():
            object_found = False
            #print(first_object)
            for attribute in first_object.get_values():
                #print(attribute)
                if attribute in rel:
                    target_attribute = rel[attribute]
                    for second_object in self.second_model_category.get_objects():
                        ## Here we search the object in the second category that has the target attribute in values
                        if target_attribute in second_object.get_values():
                            object_found = True
                            if first_object.get_id() not in join_objects:
                                join_values = first_object.get_values() + second_object.get_values()
                                print(join_values)
                                join_objects[first_object.get_id()] = AbstractObject(first_object.get_name() + " + " + second_object.get_name(), first_object.get_model(), join_values, first_object.get_id())
                            else:
                                join_objects[first_object.get_id()].append_values(second_object.get_values())
                        elif self.right == True:
                            if second_object.get_id() not in join_objects:
                                join_objects[second_object.get_id()] = AbstractObject(second_object.get_name(), second_object.get_model(), second_object.get_values(), second_object.get_id())
                            else:
                                join_objects[second_object.get_id()].append_values(second_object.get_values())           
            if self.left == True and object_found == False:
                if first_object.get_id() not in join_objects:
                    join_objects[first_object.get_id()] = AbstractObject(first_object.get_name(), first_object.get_model(), first_object.get_values(), first_object.get_id())
                else:
                    join_objects[first_object.get_id()].append_values(first_object.get_values())
        return join_objects

    def create_morphisms(self, join_objects):
        return self.create_morphisms_for_given_category(self.first_model_category, join_objects) + self.create_morphisms_for_given_category(self.second_model_category, join_objects)

    def create_morphisms_for_given_category(self, category, join_objects):
        join_morphisms = []
        for mor in category.get_morphisms():
            source_id, target_id = mor.get_source().get_id(), mor.get_target().get_id()
            join_source, join_target = None, None
            if source_id in join_objects:
                join_source = join_objects[source_id]
                if target_id in join_objects:
                    join_target = join_objects[source_id]
                    join_morphisms.append(AbstractMorphism(mor.get_name(), join_source, join_target))
        return join_morphisms


    def project_left_leg(self, rels):
        projection = []
        for rel in rels:
            values = list(rel.values())
            keys = list(rel.keys())
            keys_and_values = values + keys
            proj = dict()
            for key in keys:
                for value in keys_and_values:
                    proj[value] = key
            projection.append(proj)
        return projection

    def project_right_leg(self, rels):
        projection = []
        for rel in rels:
            values = list(rel.values())
            keys = list(rel.keys())
            keys_and_values = values + keys
            proj = dict()
            for key in values:
                for value in keys_and_values:
                    proj[value] = key
            projection.append(proj)
        return projection