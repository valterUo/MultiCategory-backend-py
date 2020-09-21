import os
from tables import *
from multi_model_db.multi_model_db import MultiModelDB
from multi_model_join.multi_model_join import MultiModelJoin
from initialization_of_demo_databases.initialize_ecommerce_morphisms import initialize_ecommerce_morphisms
from constructing_multi_model_db.collection_constructor.create_collection_constructor import create_collection_constructors
dirname = os.path.dirname(__file__)

class ECommerceMultiModelDatabase():

    def __init__(self):

        ecommerce_config = []

        customers_vertex_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\customerVertex.csv")
        customers_edge_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\customerEdge.csv")
        interest_vertex_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\interestVertex.csv")
        interest_edge_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\interestEdge.csv")
        locations_table_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\locationsTable.csv")
        orders_xml_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\orders.xml")
        sites_table_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\sites.csv")
        key_value_pairs_path = os.path.join(
            dirname, "..\\..\\original_data\\eCommerce\\keyValuePairs.json")
        target_folder = os.path.join(
            dirname, "..\\..\\db_files\\ecommerce")

        ## ===== Customer graph =====
        customer_edge_info = [{"file_path": customers_edge_path, "delimiter": ";", "schema": ["source","target"], "source_attribute_index": 0, "target_attribute_index": 1}]
        customer_vertex_info = [ { "file_path": customers_vertex_path, "schema": ["customer_id", "name", "creditLimit", "customer_locationId"], "key_attribute_index": 0, "delimiter": ";" } ]
        customer_vertex_model = ["customer_id", "name", "creditLimit", "customer_locationId"]
        ecommerce_config.append({"model": "graph", "name": "customer", "edgeInfo": customer_edge_info, "vertexInfo": customer_vertex_info, "vertexModel": customer_vertex_model, "edgeModel": ["knows"], "targetFolder": target_folder})

        ## ===== Interest graph =====
        interest_edge_info = [{"file_path": interest_edge_path, "delimiter": ";", "schema": ["customerId","targetId", "weight"], "source_attribute_index": 0, "target_attribute_index": 1}]
        interest_vertex_info = [ { "file_path": interest_vertex_path, "schema": ["interest_id", "topic", "interest_locationId"], "key_attribute_index": 0, "delimiter": ";" },
        { "file_path": customers_vertex_path, "schema": ["customer_id", "name", "creditLimit", "customer_locationId"], "key_attribute_index": 0, "delimiter": ";" } ]
        interest_vertex_model = ["customer_id", "name", "creditLimit", "customer_locationId", "interest_id", "topic", "interest_locationId"]
        ecommerce_config.append({"model": "graph", "name": "interest", "edgeInfo": interest_edge_info, "vertexInfo": interest_vertex_info, "vertexModel": interest_vertex_model, "edgeModel": ["interested"], "targetFolder": target_folder})
        
        ## ===== Location table =====
        location_attributes_datatypes = dict()
        location_attributes_datatypes["location_id"] = Int32Col()
        location_attributes_datatypes["address"] = StringCol(64, dflt='NULL')
        location_attributes_datatypes["zipCode"] = StringCol(32, dflt='NULL')
        location_attributes_datatypes["city"] = StringCol(32, dflt='NULL')
        location_attributes_datatypes["country"] = StringCol(32, dflt='NULL')
        ecommerce_config.append({"model": "relational", "name": "location", "attributes_datatypes": location_attributes_datatypes, "sourceFile": locations_table_path, "delimiter": ";", "primaryKey": "location_id", "targetFolder": target_folder})

        ## ===== Orders XML =====
        ecommerce_config.append({"model": "tree", "name": "orders", "format": "XML", "sourceFile": orders_xml_path, "targetFolder": target_folder})

        ## ===== Sites table =====
        site_attributes_datatypes = dict()
        site_attributes_datatypes["site_id"] = Int32Col()
        site_attributes_datatypes["site_locationId"] = Int32Col()
        site_attributes_datatypes["name"] = StringCol(32, dflt='NULL')
        site_attributes_datatypes["year"] = Int32Col(dflt= 0)
        site_attributes_datatypes["description"] = StringCol(64, dflt='NULL')
        ecommerce_config.append({"model": "relational", "name": "site", "attributes_datatypes": site_attributes_datatypes, "sourceFile": sites_table_path, "delimiter": ";", "primaryKey": "site_id", "targetFolder": target_folder})

        ## ===== Key-value pairs =====
        ecommerce_config.append({"model": "tree", "name": "key_value_pairs", "format": "JSON", "sourceFile": key_value_pairs_path, "targetFolder": target_folder})

        objects = create_collection_constructors(ecommerce_config)
        morphisms = initialize_ecommerce_morphisms(objects)

        self.ecommerce_multi_model_db = MultiModelDB("ecommerce multi-model database", objects, morphisms)
        

    def get_multi_model_db(self):
        return self.ecommerce_multi_model_db


    def run_multi_model_join_examples(self):
        site = self.ecommerce_multi_model_db.get_objects()["site"]
        location = self.ecommerce_multi_model_db.get_objects()["location"]
        site_to_location_morphism = self.ecommerce_multi_model_db.get_morphisms()["site_to_location_morphism"]
        
        join1 = MultiModelJoin(site, site_to_location_morphism, location)

        customer_graph = self.ecommerce_multi_model_db.get_objects()["customer"]
        customer_to_location_morphism = self.ecommerce_multi_model_db.get_morphisms()["customer_to_location_morphism"]

        join2 = MultiModelJoin(customer_graph, customer_to_location_morphism, location, True)

        customer_interest_morphism = self.ecommerce_multi_model_db.get_morphisms()["customer_interest_morphism"]
        interest_graph = self.ecommerce_multi_model_db.get_objects()["interest"]

        join3 = MultiModelJoin(customer_graph, customer_interest_morphism, interest_graph, True, True)

        location_to_customer_morphism = self.ecommerce_multi_model_db.get_morphisms()["location_to_customer_morphism"]

        description = dict()
        description["customer_id"] = StringCol(64, dflt='NULL')
        description["name"] = StringCol(64, dflt='NULL')
        description["creditLimit"] = StringCol(64, dflt='NULL')
        description["customer_locationId"] = StringCol(64, dflt='NULL')

        join4 = MultiModelJoin(location, location_to_customer_morphism, customer_graph, second_description = description)

        composition_order_to_customer = self.ecommerce_multi_model_db.get_morphisms()["composition_order_to_customer"]
        orders = self.ecommerce_multi_model_db.get_objects()["orders"]

        join5 = MultiModelJoin(orders, composition_order_to_customer, customer_graph, tree_attributes=["Orders"])