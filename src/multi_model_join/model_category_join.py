from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory

"""
model_relationship.get_relationship() = list of dictionaries
.get_objects() = list of lists
"""

def join(first_model_category, model_relationship, second_model_category):
    join_name = first_model_category.get_name() + " + " + second_model_category.get_name()
    new_objects = []
    for first_object in first_model_category.get_objects():
        try:
            for attribute in first_object:
                if type(model_relationship.get_relationship()) == list:
                    for rel in model_relationship.get_relationship():
                        if attribute in rel:
                            target_attribute = rel[attribute]
                            for second_object in second_model_category.get_objects():
                                try:
                                    if target_attribute in second_object:
                                        new_object = []
                                        for attribute1 in first_object:
                                            new_object.append(attribute1)
                                        for attribute2 in second_object:
                                            if attribute2 != target_attribute:
                                                new_object.append(attribute2)
                                        new_objects.append(new_object)
                                except:
                                    print("second_object is not iterable, the algorithm uses abstract objects", second_object)
                                    new_objects.append([second_object])
                elif type(model_relationship.get_relationship()) == dict:
                    rel = model_relationship.get_relationship()
                    if attribute in rel:
                            target_attribute = rel[attribute]
                            for second_object in second_model_category.get_objects():
                                try:
                                    if target_attribute in second_object:
                                        new_object = []
                                        for attribute1 in first_object:
                                            new_object.append(attribute1)
                                        for attribute2 in second_object:
                                            if attribute2 != target_attribute:
                                                new_object.append(attribute2)
                                        new_objects.append(new_object)
                                except:
                                    print("second_object is not iterable, the algorithm uses abstract objects", second_object)
                                    new_objects.append([second_object])
        except:
            print("first_object is not iterable, the algorithm uses abstract objects", first_object)
            new_objects.append([first_object])

    if type(first_model_category) == TableModelCategory:
        result = TableModelCategory(join_name, new_objects[0], first_model_category.get_primary_key())
    elif type(first_model_category) == GraphModelCategory:
        if len(new_objects) == 1:
            result = GraphModelCategory(join_name, new_objects[0], first_model_category.get_edge_object())
        elif len(new_objects) == 2:
            result = GraphModelCategory(join_name, new_objects[0], new_objects[1])
    elif type(first_model_category) == TreeModelCategory:
        print(new_objects)
        result = TreeModelCategory(join_name, new_objects[0])

    return result

        