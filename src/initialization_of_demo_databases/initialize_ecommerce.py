import os
from tables import *
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_tree_model import TreeModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_db.multi_model_db_instance.multi_model_db_instance import MultiModelDBInstance
from multi_model_db.multi_model_db import MultiModelDB
from multi_model_join.multi_model_join import MultiModelJoin
from initialization_of_demo_databases.initialize_ecommerce_morphisms import initialize_ecommerce_morphisms
from copy import deepcopy
dirname = os.path.dirname(__file__)
e_commerce_instance = None

class ECommerceMultiModelDatabase():

    def __init__(self):

        objects = dict()
        morphisms = dict()

        customers_vertex_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\customerVertex.csv")
        customers_edge_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\customerEdge.csv")
        interest_vertex_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\interestVertex.csv")
        interest_edge_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\interestEdge.csv")
        locations_table_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\locationsTable.csv")
        orders_xml_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\orders.xml")
        sites_table_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\sites.csv")
        key_value_pairs_path = os.path.join(
            dirname, "..\\..\\data\\eCommerce\\keyValuePairs.json")
        target_folder = os.path.join(
            dirname, "..\\..\\db_files\\ecommerce")

        ## Customer graph
        name = "customer"
        edge_info = [{"file_path": customers_edge_path, "delimiter": ";", "schema": ["source","target"], "source_attribute_index": 0, "target_attribute_index": 1}]
        vertex_info = [ { "file_path": customers_vertex_path, "schema": ["customer_id", "name", "creditLimit", "customer_locationId"], "key_attribute_index": 0, "delimiter": ";" } ]
        
        customer_graph = GraphCollection(name, vertex_info, edge_info, target_folder)
        customer_graph_model = GraphModelCategory(name, vertex_object = ["customer_id", "name", "creditLimit", "customer_locationId"], edge_object = ["knows"])
        customer_graph_collection = CollectionConstructor(name, customer_graph_model, customer_graph)
        objects[name] = customer_graph_collection

        ## Interest graph
        name = "interest"
        edge_info = [{"file_path": interest_edge_path, "delimiter": ";", "schema": ["customerId","targetId", "weight"], "source_attribute_index": 0, "target_attribute_index": 1}]
        vertex_info = [ { "file_path": interest_vertex_path, "schema": ["interest_id", "topic", "interest_locationId"], "key_attribute_index": 0, "delimiter": ";" },
        { "file_path": customers_vertex_path, "schema": ["customer_id", "name", "creditLimit", "customer_locationId"], "key_attribute_index": 0, "delimiter": ";" } ]
        
        interest_graph = GraphCollection(name, vertex_info, edge_info, target_folder)
        interest_graph_model = GraphModelCategory(name, vertex_object = ["customer_id", "name", "creditLimit", "customer_locationId", "interest_id", "topic", "interest_locationId"], edge_object=["interested"])
        interest_graph_collection = CollectionConstructor(name, interest_graph_model, interest_graph)
        
        objects[name] = interest_graph_collection

        ## Location table
        location_attributes_datatypes = dict()
        location_attributes_datatypes["location_id"] = Int32Col()
        location_attributes_datatypes["address"] = StringCol(64, dflt='NULL')
        location_attributes_datatypes["zipCode"] = StringCol(32, dflt='NULL')
        location_attributes_datatypes["city"] = StringCol(32, dflt='NULL')
        location_attributes_datatypes["country"] = StringCol(32, dflt='NULL')

        name = "location"
        primary_key = "location_id"
        location_table_model = TableModelCategory(name, list(location_attributes_datatypes.keys()), primary_key)
        location_table = TableCollection(name, location_attributes_datatypes, locations_table_path, target_folder, ";")
        location_collection = CollectionConstructor(name, location_table_model, location_table)
        objects[name] = location_collection

        ## Orders XML
        name = "orders"
        orders_tree_model = TreeModelCategory(name)
        orders_tree_collection = TreeCollection(name, orders_xml_path, target_folder, "XML")
        orders_collection = CollectionConstructor(name, orders_tree_model, orders_tree_collection)
        objects[name] = orders_collection

        ## Sites table
        site_attributes_datatypes = dict()
        site_attributes_datatypes["site_id"] = Int32Col()
        site_attributes_datatypes["site_locationId"] = Int32Col()
        site_attributes_datatypes["name"] = StringCol(32, dflt='NULL')
        site_attributes_datatypes["year"] = Int32Col(dflt= 0)
        site_attributes_datatypes["description"] = StringCol(64, dflt='NULL')

        name = "site"
        primary_key = "site_id"
        site_table_model = TableModelCategory(name, list(site_attributes_datatypes.keys()), primary_key)
        site_table = TableCollection(name, site_attributes_datatypes, sites_table_path, target_folder, ";")
        site_collection = CollectionConstructor(name, site_table_model, site_table)
        objects[name] = site_collection

        ## Key-value pairs
        name = "key_value_pairs"
        key_value_tree_model = TreeModelCategory(name)
        key_value_pairs = TreeCollection(name, key_value_pairs_path, target_folder)
        key_value_pairs_collection = CollectionConstructor(name, key_value_tree_model, key_value_pairs)
        objects[name] = key_value_pairs_collection

        morphisms = initialize_ecommerce_morphisms(objects)

        ecommerce_instance_category = MultiModelDBInstance("ecommerce instance", objects, morphisms)

        self.ecommerce_multi_model_db_instance = MultiModelDB("ecommerce multi-model database", ecommerce_instance_category)
        

    def get_instance(self):
        return self.ecommerce_multi_model_db_instance

    def run_multi_model_join_examples(self):
        site = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_objects()["site"]
        location = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_objects()["location"]
        site_to_location_morphism = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_morphisms()["site_to_location_morphism"]
        
        join1 = MultiModelJoin(site, site_to_location_morphism, location)

        customer_graph = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_objects()["customer"]
        customer_to_location_morphism = site_to_location_morphism = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_morphisms()["customer_to_location_morphism"]

        join2 = MultiModelJoin(customer_graph, customer_to_location_morphism, location, True)

        customer_interest_morphism = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_morphisms()["customer_interest_morphism"]
        interest_graph = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_objects()["interest"]

        join3 = MultiModelJoin(customer_graph, customer_interest_morphism, interest_graph, True, True)

        location_to_customer_morphism = self.ecommerce_multi_model_db_instance.get_multi_model_db_instance().get_morphisms()["location_to_customer_morphism"]

        description = dict()
        description["customer_id"] = StringCol(64, dflt='NULL')
        description["name"] = StringCol(64, dflt='NULL')
        description["creditLimit"] = StringCol(64, dflt='NULL')
        description["customer_locationId"] = StringCol(64, dflt='NULL')

        join4 = MultiModelJoin(location, location_to_customer_morphism, customer_graph, second_description = description)