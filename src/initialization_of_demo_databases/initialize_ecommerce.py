import os
from tables import *
from multi_model_db.multi_model_db import MultiModelDB
from initialization_of_demo_databases.initialize_ecommerce_morphisms import initialize_ecommerce_morphisms
from constructing_multi_model_db.collection_constructor.create_collection_constructor import create_collection_constructors
dirname = os.path.dirname(__file__)


class ECommerceMultiModelDatabase():

    def __init__(self):

        ecommerce_config = []

        customers_vertex_path = os.path.join(
            dirname, "..//..//resources//ecommerce//customerVertex.csv")
        if not os.path.exists(customers_vertex_path):
            raise FileNotFoundError("Customer vertex file not found")

        customers_edge_path = os.path.join(
            dirname, "..//..//resources//ecommerce//customerEdge.csv")
        if not os.path.exists(customers_edge_path):
            raise FileNotFoundError("Customer edge file not found")

        interest_vertex_path = os.path.join(
            dirname, "..//..//resources//ecommerce//interestVertex.csv")
        if not os.path.exists(interest_vertex_path):
            raise FileNotFoundError("Interest vertex file not found")

        interest_edge_path = os.path.join(
            dirname, "..//..//resources//ecommerce//interestEdge.csv")
        if not os.path.exists(interest_edge_path):
            raise FileNotFoundError("Interest edge file not found")

        locations_table_path = os.path.join(
            dirname, "..//..//resources//ecommerce//locationsTable.csv")
        if not os.path.exists(locations_table_path):
            raise FileNotFoundError("Locations file not found")

        orders_xml_path = os.path.join(
            dirname, "..//..//resources//ecommerce//orders.xml")
        if not os.path.exists(orders_xml_path):
            raise FileNotFoundError("Orders file not found")

        sites_table_path = os.path.join(
            dirname, "..//..//resources//ecommerce//sites.csv")
        if not os.path.exists(sites_table_path):
            raise FileNotFoundError("Sites file not found")

        key_value_pairs_path = os.path.join(
            dirname, "..//..//resources//ecommerce//keyValuePairs.json")
        if not os.path.exists(key_value_pairs_path):
            raise FileNotFoundError("Key-value pairs file not found")

        target_folder = os.path.join(
            dirname, "..//..//db_files//ecommerce")
        if not os.path.exists(target_folder):
            print("Path " + target_folder + " does not exist. Trying to create.")
            try:
                os.mkdir(target_folder)
            except OSError:
                raise FileNotFoundError("Target database folder does not exist and cannot be created")

        ## ===== Customer graph =====
        customer_edge_info = [{"file_path": customers_edge_path, "delimiter": ";", "schema": [
            "source", "target"], "source_attribute_index": 0, "target_attribute_index": 1}]
        customer_vertex_info = [{"file_path": customers_vertex_path, "schema": [
            "customer_id", "name", "creditLimit", "customer_locationId"], "key_attribute_index": 0, "delimiter": ";"}]
        customer_vertex_model = ["customer_id",
                                 "name", "creditLimit", "customer_locationId"]
        ecommerce_config.append({"model": "graph", "name": "customer", "edgeInfo": customer_edge_info, "vertexInfo": customer_vertex_info,
                                 "vertexModel": customer_vertex_model, "edgeModel": ["knows"], "targetFolder": target_folder})

        ## ===== Interest graph =====
        interest_edge_info = [{"file_path": interest_edge_path, "delimiter": ";", "schema": [
            "customerId", "targetId", "weight"], "source_attribute_index": 0, "target_attribute_index": 1}]
        interest_vertex_info = [{"file_path": interest_vertex_path, "schema": ["interest_id", "topic", "interest_locationId"], "key_attribute_index": 0, "delimiter": ";"},
                                {"file_path": customers_vertex_path, "schema": ["customer_id", "name", "creditLimit", "customer_locationId"], "key_attribute_index": 0, "delimiter": ";"}]
        interest_vertex_model = ["customer_id", "name", "creditLimit",
                                 "customer_locationId", "interest_id", "topic", "interest_locationId"]
        ecommerce_config.append({"model": "graph", "name": "interest", "edgeInfo": interest_edge_info, "vertexInfo": interest_vertex_info,
                                 "vertexModel": interest_vertex_model, "edgeModel": ["interested"], "targetFolder": target_folder})

        ## ===== Location table =====
        location_attributes_datatypes = dict()
        location_attributes_datatypes["location_id"] = Int32Col()
        location_attributes_datatypes["address"] = StringCol(64, dflt='NULL')
        location_attributes_datatypes["zipCode"] = StringCol(32, dflt='NULL')
        location_attributes_datatypes["city"] = StringCol(32, dflt='NULL')
        location_attributes_datatypes["country"] = StringCol(32, dflt='NULL')
        ecommerce_config.append({"model": "relational", "name": "location", "attributes_datatypes": location_attributes_datatypes,
                                 "sourceFile": locations_table_path, "delimiter": ";", "primaryKey": "location_id", "targetFolder": target_folder})

        ## ===== Orders XML =====
        ecommerce_config.append({"model": "tree", "name": "orders", "format": "XML",
                                 "sourceFile": orders_xml_path, "targetFolder": target_folder})

        ## ===== Sites table =====
        site_attributes_datatypes = dict()
        site_attributes_datatypes["site_id"] = Int32Col()
        site_attributes_datatypes["site_locationId"] = Int32Col()
        site_attributes_datatypes["name"] = StringCol(32, dflt='NULL')
        site_attributes_datatypes["year"] = Int32Col(dflt=0)
        site_attributes_datatypes["description"] = StringCol(64, dflt='NULL')
        ecommerce_config.append({"model": "relational", "name": "site", "attributes_datatypes": site_attributes_datatypes,
                                 "sourceFile": sites_table_path, "delimiter": ";", "primaryKey": "site_id", "targetFolder": target_folder})

        ## ===== Key-value pairs =====
        ecommerce_config.append({"model": "tree", "name": "key_value_pairs", "format": "JSON",
                                 "sourceFile": key_value_pairs_path, "targetFolder": target_folder})

        objects = create_collection_constructors(ecommerce_config)
        morphisms = initialize_ecommerce_morphisms(objects)

        self.ecommerce_multi_model_db = MultiModelDB(
            "E-commerce multi-model database", objects, morphisms, True)

    def get_multi_model_db(self):
        return self.ecommerce_multi_model_db
