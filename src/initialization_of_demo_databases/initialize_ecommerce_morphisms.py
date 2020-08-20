from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship
from supportive_functions.row_manipulations import row_to_dictionary

def initialize_ecommerce_morphisms(objects):
    ## Morphisms

    morphisms = dict()

    customer_graph = objects["customer"].get_collection()
    customer_graph_model = objects["customer"].get_model_category()
    interest_graph = objects["interest"].get_collection()
    interest_graph_model = objects["interest"].get_model_category()
    location_table = objects["location"].get_collection()
    location_table_model = objects["location"].get_model_category()
    orders_tree_collection = objects["orders"].get_collection()
    orders_tree_model = objects["orders"].get_model_category()
    site_table = objects["site"].get_collection()
    site_table_model = objects["site"].get_model_category()
    key_value_tree_model = objects["key_value_pairs"].get_model_category()
    key_value_pairs = objects["key_value_pairs"].get_collection()

    ## Every site is functionally in relationship with some location: locationId in site table -> id in location table. This is foreign key primary key pair.

    site_location_model_relationship = ModelRelationship("site_location_model_relationship", site_table_model, [{ "site_locationId": "location_id" }], location_table_model)
    site_location_collection_relationship = CollectionRelationship("site_location_model_relationship", site_table, 
                lambda site_row : [row_to_dictionary(location_row) for location_row in location_table.get_rows() if site_row['site_locationId'] == location_row["location_id"]], 
                        location_table)

    site_to_location_morphism = CollectionConstructorMorphism("site_to_location_morphism", objects["site"], site_location_model_relationship, site_location_collection_relationship, objects["location"])
    morphisms["site_to_location_morphism"] = site_to_location_morphism

    ## Every customer is assigned with a location

    customer_location_model_relationship = ModelRelationship("customer_location_model_relationship", customer_graph_model, [{ "customer_locationId": "location_id" }], location_table_model)
    customer_location_collection_relationship = CollectionRelationship("customer_location_model_relationship", customer_graph, 
                lambda customer : [row_to_dictionary(location_row) for location_row in location_table.get_rows() if len(customer) == 2 and int(customer[1]['customer_locationId']) == location_row["location_id"]], 
                        location_table)

    customer_to_location_morphism = CollectionConstructorMorphism("customer_to_location_morphism", objects["customer"], customer_location_model_relationship, customer_location_collection_relationship, objects["location"])
    morphisms["customer_to_location_morphism"] = customer_to_location_morphism

    ## Some customers in the interest graph are same as some customers in customers graph

    customer_interest_model_relationship = ModelRelationship("customer_model_relationship", customer_graph_model, [{ "customer_id": "interest_id" }], interest_graph_model)
    customer_interest_collection_relationship = CollectionRelationship("customer_interest_model_relationship", customer_graph, 
                lambda customer : [customer2 for customer2 in interest_graph.get_iterable_collection_of_objects()], 
                        interest_graph)

    customer_interest_morphism = CollectionConstructorMorphism("customer_interest_morphism", objects["customer"], customer_interest_model_relationship, customer_interest_collection_relationship, objects["interest"])
    morphisms["customer_interest_morphism"] = customer_interest_morphism

    ## Morphism from one to many

    location_to_customer_model_relationship = ModelRelationship("location_to_customer_relationship", location_table_model, [{ "location_id": "customer_id" }], customer_graph_model)
    location_to_customer_collection_relationship = CollectionRelationship("customer_interest_model_relationship", location_table, 
                lambda location : [customer for customer in customer_graph.get_iterable_collection_of_objects() if len(customer) == 2 and customer[1]["customer_locationId"] == str(location["location_id"])], 
                        customer_graph)

    location_to_customer_morphism = CollectionConstructorMorphism("location_to_customer_morphism", objects["location"], location_to_customer_model_relationship, location_to_customer_collection_relationship, objects["interest"])
    morphisms["location_to_customer_morphism"] = location_to_customer_morphism

    return morphisms