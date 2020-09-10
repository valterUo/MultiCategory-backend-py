from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship
from supportive_functions.row_manipulations import row_to_dictionary

def create_collection_constructor_morphisms(config, objects):
    morphisms = dict()
    for info in config:
        name = info["name"]
        source = objects[info["source"]]
        target = objects[info["target"]]
        source_model = source.get_model_category()
        target_model = target.get_model_category()
        source_collection = source.get_collection()
        target_collection = target.get_collection()
        model_relationship = ModelRelationship(name, source_model, info["modelRelationship"], target_model)
        collection_relationship = CollectionRelationship(name, source_collection, info["lambda"], target_collection)
        morphisms[name] = CollectionConstructorMorphism(name, source, model_relationship, collection_relationship, target)
    return morphisms