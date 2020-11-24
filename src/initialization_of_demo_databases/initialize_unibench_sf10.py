import os
from tables import *
from multi_model_db.multi_model_db import MultiModelDB
from constructing_multi_model_db.collection_constructor.create_collection_constructor import create_collection_constructors

class UnibenchMultiModelDatabase():

    def __init__(self, version = "SF10"):

        unibench_config = []

        base_path = "E://MultiCategory//original_files//Unibench_SF10"

        customer_data_path = base_path + "//Customer//person_0_0.csv"
        feedback_data_path = base_path + "//Feedback//feedback.csv"
        order_data_path = base_path + "//Order//order.json"
        product_data_path = base_path + "//Product//Product.csv"
        post_data_path = base_path + "//SocialNetwork//post_0_0.csv"
        vendor_data_path = base_path + "//Vendor//vendor.csv"
        person_knows_person_data_path = base_path + "//SocialNetwork//person_knows_person_0_0.csv"
        post_hasCreator_person_data_path = base_path + "//SocialNetwork//post_hasCreator_person_0_0.csv"
        post_hasTag_tag_data_path = base_path + "//SocialNetwork//post_hasTag_tag_0_0.csv"
        target_folder = "E://MultiCategory//db_files//Unibench_SF10"

        if version == "SF30":
            base_path = "E://MultiCategory//original_files//Unibench_SF30"
            customer_data_path = base_path + "//Customer//person_0_0.csv"
            feedback_data_path = base_path + "//Feedback//feedback.csv"
            order_data_path = base_path + "//Order//order.json"
            product_data_path = base_path + "//Product//Product.csv"
            post_data_path = base_path + "//SocialNetwork//post_0_0.csv"
            vendor_data_path = base_path + "//Vendor//vendor.csv"
            person_knows_person_data_path = base_path + "//SocialNetwork//person_knows_person_0_0.csv"
            post_hasCreator_person_data_path = base_path + "//SocialNetwork//post_hasCreator_person_0_0.csv"
            post_hasTag_tag_data_path = base_path + "//SocialNetwork//post_hasTag_tag_0_0.csv"
            target_folder = "E://MultiCategory//db_files//Unibench_SF30"


        ## ===== Customer graph =====
        customer_edge_info = [{"file_path": person_knows_person_data_path, "delimiter": "|", "schema": ["from", "to", "creationDate"], "source_attribute_index": 0, "target_attribute_index": 1}]
        customer_vertex_info = [ { "file_path": customer_data_path, "schema": ["id", "firstName", "lastName", "gender", "birthday", "creationDate", "locationIP", "browserUsed"], "key_attribute_index": 0, "delimiter": "|" } ]
        customer_vertex_model = ["id", "firstName", "lastName", "gender", "birthday", "creationDate", "locationIP", "browserUsed"]
        unibench_config.append({"model": "graph", "name": "customer", "edgeInfo": customer_edge_info, "vertexInfo": customer_vertex_info, "vertexModel": customer_vertex_model, "edgeModel": ["knows"], "targetFolder": target_folder})


        ## ===== Feedback table =====
        feedback_attributes_datatypes = dict()
        feedback_attributes_datatypes["asin"] = StringCol(34, dflt='NULL')
        feedback_attributes_datatypes["PersonId"] = StringCol(34, dflt='NULL')
        feedback_attributes_datatypes["feedback"] = StringCol(1000, dflt='NULL')
        unibench_config.append({"model": "relational", "name": "feedback", "attributes_datatypes": feedback_attributes_datatypes, "sourceFile": feedback_data_path, "delimiter": "|", "targetFolder": target_folder})


        ## ===== Product table =====
        product_attributes_datatypes = dict()
        product_attributes_datatypes["asin"] = StringCol(32, dflt='NULL')
        product_attributes_datatypes["title"] = StringCol(64, dflt='NULL')
        product_attributes_datatypes["price"] = Float32Col()
        product_attributes_datatypes["imgUrl"] = StringCol(64, dflt='NULL')
        product_attributes_datatypes["productId"] = Int32Col()
        product_attributes_datatypes["brand"] = StringCol(32, dflt='NULL')
        unibench_config.append({"model": "relational", "name": "product", "attributes_datatypes": product_attributes_datatypes, "sourceFile": product_data_path, "primaryKey": "productId", "delimiter": ",", "targetFolder": target_folder})


        ## ===== Vendor table ===== id,name,country,cdf,industry
        vendor_attributes_datatypes = dict()
        vendor_attributes_datatypes["id"] = Int32Col()
        vendor_attributes_datatypes["name"] = StringCol(34, dflt='NULL')
        vendor_attributes_datatypes["country"] = StringCol(32, dflt='NULL')
        vendor_attributes_datatypes["cdf"] = StringCol(34, dflt='NULL')
        vendor_attributes_datatypes["industry"] = StringCol(32, dflt='NULL')
        unibench_config.append({"model": "relational", "name": "vendor", "attributes_datatypes": vendor_attributes_datatypes, "sourceFile": vendor_data_path, "primaryKey": "id", "delimiter": ",", "targetFolder": target_folder})


        ## ===== Post table =====
        post_attributes_datatypes = dict()
        post_attributes_datatypes["id"] = Int64Col()
        post_attributes_datatypes["imageFile"] = StringCol(16, dflt='NULL')
        post_attributes_datatypes["creationDate"] = StringCol(32, dflt='NULL')
        post_attributes_datatypes["locationIP"] = StringCol(16, dflt='NULL')
        post_attributes_datatypes["browserUsed"] = StringCol(16, dflt='NULL')
        post_attributes_datatypes["language"] = StringCol(16, dflt='NULL')
        post_attributes_datatypes["content"] = StringCol(500, dflt='NULL')
        post_attributes_datatypes["length"] = Int32Col()
        unibench_config.append({"model": "relational", "name": "post", "attributes_datatypes": post_attributes_datatypes, "sourceFile": post_data_path, "primaryKey": "id", "delimiter": "|", "targetFolder": target_folder})
        

        ## ===== Post has tag graph =====
        post_hasTag_tag_edge_info = [{"file_path": post_hasTag_tag_data_path, "delimiter": "|", "schema": ["PostId", "TagId"], "source_attribute_index": 0, "target_attribute_index": 1}]
        post_hasTag_tag_vertex_info = []
        post_hasTag_tag_vertex_model = ["PostId", "TagId"]
        unibench_config.append({"model": "graph", "name": "post_hasTag_tag", "edgeInfo": post_hasTag_tag_edge_info, "vertexInfo": post_hasTag_tag_vertex_info, "vertexModel": post_hasTag_tag_vertex_model, "edgeModel": ["knows"], "targetFolder": target_folder})


        ## ===== Post has creator person =====
        post_hasCreator_person_edge_info = [{"file_path": post_hasCreator_person_data_path, "delimiter": "|", "schema": ["PostId", "PersonId"], "source_attribute_index": 0, "target_attribute_index": 1}]
        post_hasCreator_person_vertex_info = []
        post_hasCreator_person_vertex_model = ["PostId", "PersonId"]
        unibench_config.append({"model": "graph", "name": "post_is_created_by_person", "edgeInfo": post_hasCreator_person_edge_info, "vertexInfo": post_hasCreator_person_vertex_info, "vertexModel": post_hasCreator_person_vertex_model, "edgeModel": ["createdBy"], "targetFolder": target_folder})


        ## ===== Order =====
        unibench_config.append({"model": "tree", "name": "orders", "format": "JSON", "sourceFile": order_data_path, "targetFolder": target_folder})

        morphisms = create_collection_constructors(unibench_config)
        