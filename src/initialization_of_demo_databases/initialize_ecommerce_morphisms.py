from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship
from supportive_functions.row_manipulations import row_to_dictionary
from constructing_multi_model_db.collection_constructor.create_collection_constructor_morphism import create_collection_constructor_morphisms


def initialize_ecommerce_morphisms(objects):
    ## Morphisms

    ecommerce_morphisms_config = []

    ## Every site is functionally in relationship with some location: locationId in site table -> id in location table. This is foreign key primary key pair.

    ecommerce_morphisms_config.append({'name': 'site_to_location_morphism', 'source': 'site', 'target': 'location', 'modelRelationship': [{"site_locationId": "location_id"}], 'lambda': lambda site_row: [
                                      row_to_dictionary(location_row) for location_row in objects["location"].get_iterable_collection_of_objects() if site_row['site_locationId'] == location_row["location_id"]]})

    ## Every customer is assigned with a location

    ecommerce_morphisms_config.append({'name': 'customer_to_location_morphism', 'source': 'customer', 'target': 'location', 'modelRelationship': [{"customer_locationId": "location_id"}], 'lambda': lambda customer: [
                                      row_to_dictionary(location_row) for location_row in objects["location"].get_iterable_collection_of_objects() if len(customer) == 2 and int(customer[1]['customer_locationId']) == location_row["location_id"]]})

    ## Some customers in the interest graph are same as some customers in customers graph

    ecommerce_morphisms_config.append({'name': 'customer_interest_morphism', 'source': 'customer', 'target': 'interest', 'modelRelationship': [
                                      {"customer_id": "interest_id"}], 'lambda': lambda customer: [customer2 for customer2 in objects["interest"].get_iterable_collection_of_objects()]})

    ## Morphism from one to many

    ecommerce_morphisms_config.append({'name': 'location_to_customer_morphism', 'source': 'location', 'target': 'customer', 'modelRelationship': [{"location_id": "customer_id"}], 'lambda': lambda location: [
                                      customer for customer in objects["customer"].get_iterable_collection_of_objects() if len(customer) == 2 and customer[1]["customer_locationId"] == str(location["location_id"])]})

    ## Example with composition: orders xml -> key values pair: order to customer -> customer graph => orders xml -> customer graph
    ## key value pairs -> customer

    ecommerce_morphisms_config.append({'name': 'order_id_to_customer_morphism', 'source': 'key_value_pairs', 'target': 'customer', 'modelRelationship': [{"order_id": "customer_id"}], 'lambda': lambda elem: [
                                      customer for customer in objects["customer"].get_iterable_collection_of_objects() if len(customer) == 2 and str(elem["customer_id"]) == customer[1]["customer_id"]]})

    ## orders -> key value pairs

    ecommerce_morphisms_config.append({'name': 'order_to_customer_id_morphism', 'source': 'orders', 'target': 'key_value_pairs', 'modelRelationship': [{"Order_no": "order_id"}], 'lambda': lambda order: [
                                      elem for elem in objects["key_value_pairs"].get_iterable_collection_of_objects()["orders_to_customers"] if order["Order_no"] == elem["order_id"]]})

    ## Example with composition: orders xml -> key values pair: order to customer -> customer graph => orders xml -> customer graph

    morphisms = create_collection_constructor_morphisms(
        ecommerce_morphisms_config, objects)

    composition_order_to_customer = morphisms["order_id_to_customer_morphism"].compose(
        morphisms["order_to_customer_id_morphism"])
    morphisms["composition_order_to_customer"] = composition_order_to_customer

    return morphisms