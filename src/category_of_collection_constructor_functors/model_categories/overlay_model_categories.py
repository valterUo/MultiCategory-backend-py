from category_of_collection_constructor_functors.model_categories.general_model_category import GenericModelCategory
from abstract_category.abstract_object import AbstractObject
from abstract_category.abstract_morphism import AbstractMorphism

def overlay_model_categories(first, object_id1, second, object_id2):
    new_objects, new_morphisms, models = [], [], []
    new_id, overlaid_object = None, None
    for obj1 in first.get_objects():
        if obj1.get_id() == object_id1:
            for obj2 in second.get_objects():
                if obj2.get_id() == object_id2:
                    new_values = None
                    if obj1.get_values() != None and obj2.get_values() != None:
                        new_values = obj1.get_values() + obj2.get_values()
                    elif obj1.get_values() != None:
                        new_values = obj1.get_values()
                    elif obj2.get_values() != None:
                        new_values = obj2.get_values()
                    overlaid_object = AbstractObject(obj1.get_name() + " + " + obj2.get_name(), obj1.get_model() + " with " + obj2.get_model(), new_values)
                    new_id = overlaid_object.get_id()
                    new_objects.append(overlaid_object)
                    break
            break

    for obj1 in first.get_objects():
        if obj1.get_id() != object_id1:
            new_objects.append(obj1)

    for obj2 in second.get_objects():
        if obj2.get_id() != object_id2:
            new_objects.append(obj2)
        
    for mor1 in first.get_morphisms():
        if mor1.get_source().get_id() == obj1.get_id():
            new_morphisms.append(AbstractMorphism(mor1.get_name(), overlaid_object, mor1.get_target(), mor1.get_model()))
        elif mor1.get_target().get_id() == obj1.get_id():
            new_morphisms.append(AbstractMorphism(mor1.get_name(), mor1.get_target(),overlaid_object, mor1.get_model()))

    for mor2 in second.get_morphisms():
        if mor2.get_source().get_id() == obj2.get_id():
            new_morphisms.append(AbstractMorphism(mor2.get_name(), overlaid_object, mor2.get_target(), mor2.get_model()))
        elif mor2.get_target().get_id() == obj2.get_id():
            new_morphisms.append(AbstractMorphism(mor2.get_name(), mor2.get_target(),overlaid_object, mor2.get_model()))
    
    return GenericModelCategory(first.get_name() + ' + ' + second.get_name(), new_objects, new_morphisms, models)