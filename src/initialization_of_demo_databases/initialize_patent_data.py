from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from tables import *
from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from multi_model_db.multi_model_db_instance.multi_model_db_instance import MultiModelDBInstance
from multi_model_db.multi_model_db import MultiModelDB
from category_of_collection_constructor_functors.model_categories.model_relationship import ModelRelationship
from category_of_collection_constructor_functors.collections.collection_relationship import CollectionRelationship
from category_of_collection_constructor_functors.collection_constructor_morphism import CollectionConstructorMorphism
import os
dirname = os.path.dirname(__file__)

class PatentMultiModelDatabase:

    def __init__(self):
        objects = dict()
        morphisms = dict()

        assignee_data_path = os.path.join(
            dirname, "..\\..\\original_data\\patent\\assignee.table")
        category_data_path = os.path.join(
            dirname, "..\\..\\original_data\\patent\\category.table")
        citation_data_path = os.path.join(
            dirname, "..\\..\\original_data\\patent\\citation.graph")
        class_data_path = os.path.join(
            dirname, "..\\..\\original_data\\patent\\class.table")
        inventor_data_path = os.path.join(
            dirname, "..\\..\\original_data\\patent\\inventor.table")
        patent_data_path = os.path.join(
            dirname, "..\\..\\original_data\\patent\\patent.table")
        target_folder = os.path.join(
            dirname, "..\\..\\db_files\\patent")

        ## Patent table

        patent_attributes_datatypes = dict()
        patent_attributes_datatypes["PATENT"] = StringCol(64)
        patent_attributes_datatypes["GYEAR"] = StringCol(64)
        patent_attributes_datatypes["GDATE"] = StringCol(64)
        patent_attributes_datatypes["APPYEAR"] = StringCol(64)
        patent_attributes_datatypes["COUNTRY"] = StringCol(64)
        patent_attributes_datatypes["POSTATE"] = StringCol(64)
        patent_attributes_datatypes["ASSIGNEE"] = StringCol(64)
        patent_attributes_datatypes["ASSCODE"] = StringCol(64)
        patent_attributes_datatypes["CLAIMS"] = StringCol(64)
        patent_attributes_datatypes["NCLASS"] = StringCol(64)
        patent_attributes_datatypes["CAT"] = StringCol(64)
        patent_attributes_datatypes["SUBCAT"] = StringCol(64)
        patent_attributes_datatypes["CMADE"] = StringCol(64)
        patent_attributes_datatypes["CRECEIVE"] = StringCol(64)
        patent_attributes_datatypes["RATIOCIT"] = StringCol(64)
        patent_attributes_datatypes["GENERAL"] = StringCol(64)
        patent_attributes_datatypes["ORIGINAL"] = StringCol(64)
        patent_attributes_datatypes["FWDAPLAG"] = StringCol(64)
        patent_attributes_datatypes["BCKGTLAG"] = StringCol(64)
        patent_attributes_datatypes["SELFCTUB"] = StringCol(64)
        patent_attributes_datatypes["SELFCTLB"] = StringCol(64)
        patent_attributes_datatypes["SECDUPBD"] = StringCol(64)
        patent_attributes_datatypes["SECDLWBD"] = StringCol(64)

        patent_table = TableCollection("patent", patent_attributes_datatypes, patent_data_path, target_folder, ",")
        patent_table_model = TableModelCategory("patent", patent_attributes_datatypes, "PATENT")
        patent_collection = CollectionConstructor("patent", patent_table_model, patent_table)

        ## Inventor table

        inventor_attributes_datatypes = dict()
        inventor_attributes_datatypes["PATENT"] = StringCol(64)
        inventor_attributes_datatypes["LASTNAM"] = StringCol(64)
        inventor_attributes_datatypes["FIRSTNAM"] = StringCol(64)
        inventor_attributes_datatypes["MIDNAM"] = StringCol(64)
        inventor_attributes_datatypes["MODIFNAM"] = StringCol(64)
        inventor_attributes_datatypes["STREET"] = StringCol(64)
        inventor_attributes_datatypes["CITY"] = StringCol(64)
        inventor_attributes_datatypes["POSTATE"] = StringCol(64)
        inventor_attributes_datatypes["COUNTRY"] = StringCol(64)
        inventor_attributes_datatypes["ZIP"] = StringCol(64) 
        inventor_attributes_datatypes["INVSEQ"] = StringCol(64)

        inventor_table = TableCollection("inventor", inventor_attributes_datatypes, inventor_data_path, target_folder, ",")
        inventor_table_model = TableModelCategory("inventor", inventor_attributes_datatypes)
        inventor_collection = CollectionConstructor("inventor", inventor_table_model, inventor_table)

        ## Assignee table

        assignee_attributes_datatypes = dict()
        assignee_attributes_datatypes["ASSIGNEE"] = StringCol(64)
        assignee_attributes_datatypes["ASSNAME"] = StringCol(64)
        assignee_attributes_datatypes["CNAME"] = StringCol(64)
        assignee_attributes_datatypes["CUSIP"] = StringCol(64)
        assignee_attributes_datatypes["OWN"] = StringCol(64)
        assignee_attributes_datatypes["PNAME"] = StringCol(64)
        assignee_attributes_datatypes["SNAME"] = StringCol(64)

        assignee_table = TableCollection("assignee", assignee_attributes_datatypes, assignee_data_path, target_folder, ",")
        assignee_table_model = TableModelCategory("assignee", assignee_attributes_datatypes, "ASSIGNEE")
        assignee_collection = CollectionConstructor("assignee", assignee_table_model, assignee_table)

        ## Category table

        category_attributes_datatypes = dict()
        category_attributes_datatypes["CAT"] = StringCol(64)
        category_attributes_datatypes["SUBCAT"] = StringCol(64)
        category_attributes_datatypes["SUBCATNAME"] = StringCol(64)
        category_attributes_datatypes["CATNAMESHORT"] = StringCol(64)
        category_attributes_datatypes["CATENAMELONG"] = StringCol(64)

        category_table = TableCollection("category", category_attributes_datatypes, category_data_path, target_folder, ",")
        category_table_model = TableModelCategory("category", category_attributes_datatypes, "CAT")
        category_collection = CollectionConstructor("category", category_table_model, category_table)

        ## Class table

        class_attributes_datatypes = dict()
        class_attributes_datatypes["CLASS"] = StringCol(64)
        class_attributes_datatypes["CNAME"] = StringCol(64)
        class_attributes_datatypes["SUBCAT"] = StringCol(64)
        class_attributes_datatypes["CAT"] = StringCol(64)

        class_table = TableCollection("class", class_attributes_datatypes, class_data_path, target_folder, ",")
        class_table_model = TableModelCategory("class", class_attributes_datatypes, "CLASS")
        class_collection = CollectionConstructor("class", class_table_model, class_table)

        ## Citation graph

        edge_info = [{"file_path": citation_data_path, "delimiter": ",", "schema": ["CITING","CITED"], "source_attribute_index": 0, "target_attribute_index": 1}]
        vertex_info = []
        citation_graph = GraphCollection("citation", vertex_info, edge_info, target_folder)
        citation_graph_model = GraphModelCategory("citation", vertex_schema = { "PATENTID": "String" })
        citation_graph_collection = CollectionConstructor("citation", citation_graph_model, citation_graph)

        ## Collect the functors together to form the collection of objects

        objects["patent"] = patent_collection
        objects["inventor"] = inventor_collection
        objects["assignee"] = assignee_collection
        objects["category"] = category_collection
        objects["class"] = class_collection
        objects["citation"] = citation_graph_collection

        ## Next we create some morphisms i.e. relationships between the collections. The following relationships can be considered to be initial. By the definition the relationship is defined
        ## to be a pair of functors such that the certain diagram commutes.

        ## Each node in the citation graph is functionally in a relationship with a unique row in the patent table: PATENTID  in graph nodes --> PATENT in patent table

        citation_patent_model_relationship = ModelRelationship("citation_patent_model_relationship", citation_graph_model, { "PATENTID": "PATENT" }, patent_table_model)
        citation_patent_collection_relationship = CollectionRelationship("citation_patent_collection_relationship", citation_graph_collection, 
                                                        lambda patentid : [ x for x in patent_collection.get_collection().get_rows() if x['PATENT'] == patentid], 
                                                                patent_collection)

        ## This data all together forms the following morphism

        citation_to_patent_morphism = CollectionConstructorMorphism("citation_to_patent_morphism", citation_graph_collection, citation_patent_model_relationship, citation_patent_collection_relationship, patent_collection)
        morphisms["citation_to_patent_morphism"] = citation_to_patent_morphism

        ## Every row in the inventor table is functionally in a relationship with a unique row in the patent table: PATENT in inventor table --> PATENT in patent table

        inventor_patent_model_relationship = ModelRelationship("inventor_patent_model_relationship", inventor_table_model, { "PATENT": "PATENT" }, patent_table_model)
        inventor_patent_collection_relationship = CollectionRelationship("inventor_patent_collection_relationship", inventor_table, 
                                                        lambda inventor_patent : [ x for x in patent_collection.get_collection().get_rows() if x['PATENT'] == inventor_patent], 
                                                                patent_collection)

        inventor_to_patent_morphism = CollectionConstructorMorphism("inventor_to_patent_morphism", inventor_collection, inventor_patent_model_relationship, inventor_patent_collection_relationship, patent_collection)
        morphisms["inventor_to_patent_morphism"] = inventor_to_patent_morphism

        ## Each row in the patent table is functionally in a relationship with a unique row in the assignee table: ASSIGNEE in patent table --> ASSIGNEE in assignee table

        patent_assignee_model_relationship = ModelRelationship("patent_assignee_model_relationship", patent_table_model, { "ASSIGNEE": "ASSIGNEE" }, assignee_table_model)
        patent_assignee_collection_relationship = CollectionRelationship("patent_assignee_collection_relationship", patent_table, 
                                                        lambda assignee_id : [ x for x in assignee_collection.get_collection().get_rows() if x['ASSIGNEE'] == assignee_id], 
                                                                assignee_collection)

        patent_to_assignee_morphism = CollectionConstructorMorphism("patent_to_assignee_morphism", patent_collection, patent_assignee_model_relationship, patent_assignee_collection_relationship, assignee_collection)
        morphisms["patent_to_assignee_morphism"] = patent_to_assignee_morphism

        ## Each row in the patent table is functionally in a relationship with a unique row in the class table: NCLASS in patent table --> CLASS in class table

        patent_class_model_relationship = ModelRelationship("patent_class_model_relationship", patent_table_model, { "NCLASS": "CLASS" }, class_table_model)
        patent_class_collection_relationship = CollectionRelationship("patent_class_collection_relationship", patent_table, 
                                                        lambda nclass : [ x for x in class_collection.get_collection().get_rows() if x['CLASS'] == nclass], 
                                                                class_collection)

        patent_to_class_morphism = CollectionConstructorMorphism("patent_to_class_morphism", patent_collection, patent_class_model_relationship, patent_class_collection_relationship, class_collection)
        morphisms["patent_to_class_morphism"] = patent_to_class_morphism

        ## Each row in the patent table is functionally in a relationship with a unique row in the category table: CAT in patent table --> CAT in category table

        patent_category_model_relationship = ModelRelationship("patent_category_model_relationship", patent_table_model, { "CAT": "CAT" }, class_table_model)
        patent_category_collection_relationship = CollectionRelationship("patent_category_collection_relationship", patent_table, 
                                                        lambda cat : [ x for x in category_collection.get_collection().get_rows() if x['CAT'] == cat], 
                                                                category_collection)

        patent_to_category_morphism = CollectionConstructorMorphism("patent_to_category_morphism", patent_collection, patent_category_model_relationship, patent_category_collection_relationship, category_collection)
        morphisms["patent_to_category_morphism"] = patent_to_category_morphism

        ## Each row in the patent table is functionally in a relationship with a unique row in the category table: SUBCAT in patent table --> CAT in category table

        patent_subcategory_model_relationship = ModelRelationship("patent_subcategory_model_relationship", patent_table_model, { "SUBCAT": "CAT" }, category_table_model)
        patent_subcategory_collection_relationship = CollectionRelationship("patent_subcategory_collection_relationship", patent_table, 
                                                        lambda nclass : [ x for x in category_collection.get_collection().get_rows() if x['CAT'] == nclass], 
                                                                category_collection)

        patent_to_subcategory_morphism = CollectionConstructorMorphism("patent_to_subcategory_morphism", patent_collection, patent_subcategory_model_relationship, patent_subcategory_collection_relationship, category_collection)
        morphisms["patent_to_subcategory_morphism"] = patent_to_subcategory_morphism

        ## After creating the relationships, we collect them together so that they form a category

        patent_instance_category = MultiModelDBInstance("patent instance", objects, morphisms)

        ## Eventually multi-model database is similarly a functor pointing from the instance to the schema
        ## We do not need to define the schema because it is extracted automatically from the instance

        self.patent_multi_model_database_instance = MultiModelDB("patent multi-model database", patent_instance_category)

    def get_instance(self):
        return self.patent_multi_model_database_instance
