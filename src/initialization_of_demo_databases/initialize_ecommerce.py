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
        vertex_info = [ { "file_path": customers_vertex_path, "schema": ["id", "name", "creditLimit", "locationId"], "key_attribute_index": 0, "delimiter": ";" } ]
        customer_graph = GraphCollection(name, vertex_info, edge_info, target_folder)
        customer_graph_model = GraphModelCategory(name, vertex_schema = { "id": "String", "name": "String", "creditLimit": "Int", "locationId": "Int" })
        customer_graph_collection = CollectionConstructor(name, customer_graph_model, customer_graph)
        morphisms[name] = customer_graph_collection

        ## Interest graph
        name = "interest"
        edge_info = [{"file_path": interest_edge_path, "delimiter": ";", "schema": ["customerId","targetId", "weight"], "source_attribute_index": 0, "target_attribute_index": 1}]
        vertex_info = [ { "file_path": interest_vertex_path, "schema": ["id", "topic", "locationId"], "key_attribute_index": 0, "delimiter": ";" },
        { "file_path": customers_vertex_path, "schema": ["id", "name", "creditLimit", "locationId"], "key_attribute_index": 0, "delimiter": ";" } ]
        interest_graph = GraphCollection(name, vertex_info, edge_info, target_folder)
        interest_graph_model = GraphModelCategory(name, vertex_schema = { "id": "String", "name": "String", "creditLimit": "Int", "locationId": "Int", "topic": "String" })
        interest_graph_collection = CollectionConstructor(name, interest_graph_model, interest_graph)
        morphisms[name] = interest_graph_collection

        ## Location table
        location_attributes_datatypes = dict()
        location_attributes_datatypes["id"] = Int32Col()
        location_attributes_datatypes["address"] = StringCol(64)
        location_attributes_datatypes["zipCode"] = StringCol(32)
        location_attributes_datatypes["city"] = StringCol(32)
        location_attributes_datatypes["country"] = StringCol(32)

        name = "location"
        primary_key = "id"
        location_table_model = TableModelCategory(name, location_attributes_datatypes, primary_key)
        location_table = TableCollection(name, location_attributes_datatypes, locations_table_path, target_folder, ";")
        location_collection = CollectionConstructor(name, location_table_model, location_table)
        morphisms[name] = location_collection

        ## Orders XML

        name = "orders"
        orders_tree_model = TreeModelCategory(name)
        orders_tree_collection = TreeCollection(name, orders_xml_path, target_folder, "XML")
        orders_collection = CollectionConstructor(name, orders_tree_model, orders_tree_collection)
        morphisms[name] = orders_collection

        ## Sites table
        site_attributes_datatypes = dict()
        site_attributes_datatypes["id"] = Int32Col()
        site_attributes_datatypes["locationId"] = Int32Col()
        site_attributes_datatypes["name"] = StringCol(32)
        site_attributes_datatypes["year"] = Int32Col()
        site_attributes_datatypes["description"] = StringCol(64)

        name = "site"
        primary_key = "id"
        site_table_model = TableModelCategory(name, site_attributes_datatypes, primary_key)
        site_table = TableCollection(name, site_attributes_datatypes, sites_table_path, target_folder, ";")
        site_collection = CollectionConstructor(name, site_table_model, site_table)
        morphisms[name] = site_collection

        ## Key-value pairs
        name = "key_value_pairs"
        key_value_tree_model = TreeModelCategory(name)
        key_value_pairs = TreeCollection(name, key_value_pairs_path, target_folder)
        key_value_pairs_collection = CollectionConstructor(name, key_value_tree_model, key_value_pairs)
        morphisms[name] = key_value_pairs_collection

        ## Morphisms

        ## Every site is functionally in relationship with some location: locationId in site table -> id in location table. This is foreign 

        inventor_patent_model_relationship = ModelRelationship("inventor_patent_model_relationship", inventor_table_model, { "locationId": "id" }, patent_table_model)
        inventor_patent_collection_relationship = CollectionRelationship("inventor_patent_collection_relationship", inventor_table, 
                                                        lambda inventor_patent : [ x for x in patent_collection.get_collection().get_rows() if x['PATENT'] == inventor_patent], 
                                                                patent_collection)

        inventor_to_patent_morphism = CollectionConstructorMorphism("inventor_to_patent_morphism", inventor_collection, inventor_patent_model_relationship, inventor_patent_collection_relationship, patent_collection)
        morphisms["inventor_to_patent_morphism"] = inventor_to_patent_morphism

        ecommerce_instance_category = MultiModelDBInstance("ecommerce instance", objects, morphisms)

        self.ecommerce_multi_model_db_instance = MultiModelDB("ecommerce multi-model database", ecommerce_instance_category)
        

    def get_instance(self):
        return self.ecommerce_multi_model_db_instance