from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from tables import *
from category_of_collection_constructor_functors.collections.graph_collection import GraphCollection
from category_of_collection_constructor_functors.model_categories.category_of_graph_model import GraphModelCategory
from category_of_collection_constructor_functors.model_categories.category_of_table_model import TableModelCategory
from category_of_collection_constructor_functors.collection_constructor import CollectionConstructor
from initialization_of_demo_databases.initialize_patent_morphisms import initialize_patent_morphisms
from multi_model_db.multi_model_db import MultiModelDB
import os
dirname = os.path.dirname(__file__)


class PatentMultiModelDatabase():

    def __init__(self):
        objects = dict()
        morphisms = dict()

        assignee_data_path = os.path.join(
            dirname, "..//..//resources//patent//assignee.table")
        if not os.path.exists(assignee_data_path):
            raise FileNotFoundError("Assignee file not found")

        category_data_path = os.path.join(
            dirname, "..//..//resources//patent//category.table")
        if not os.path.exists(category_data_path):
            raise FileNotFoundError("Category file not found")

        citation_data_path = os.path.join(
            dirname, "..//..//resources//patent//citation.graph")
        if not os.path.exists(citation_data_path):
            raise FileNotFoundError("Citation graph file not found")

        class_data_path = os.path.join(
            dirname, "..//..//resources//patent//class.table")
        if not os.path.exists(class_data_path):
            raise FileNotFoundError("Class file not found")

        inventor_data_path = os.path.join(
            dirname, "..//..//resources//patent//inventor.table")
        if not os.path.exists(inventor_data_path):
            raise FileNotFoundError("Inventor file not found")

        patent_data_path = os.path.join(
            dirname, "..//..//resources//patent//patent.table")
        if not os.path.exists(patent_data_path):
            raise FileNotFoundError("Patent file not found")

        # target_folder = os.path.join(
        #     dirname, "..//..//db_files//patent")
        target_folder = "E://MultiCategory//db_files//patent"
        if not os.path.exists(target_folder):
            print("Path " + target_folder + " does not exist. Trying to create.")
            try:
                os.mkdir(target_folder)
            except OSError:
                raise FileNotFoundError(
                    "Target folder not found and cannot be created")

        ## Constructing objects
        ## Patent table

        patent_attributes_datatypes = dict()
        patent_attributes_datatypes["PATENT"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["GYEAR"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["GDATE"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["APPYEAR"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["COUNTRY"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["POSTATE"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["ASSIGNEE"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["ASSCODE"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["CLAIMS"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["NCLASS"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["CAT"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["SUBCAT"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["CMADE"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["CRECEIVE"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["RATIOCIT"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["GENERAL"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["ORIGINAL"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["FWDAPLAG"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["BCKGTLAG"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["SELFCTUB"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["SELFCTLB"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["SECDUPBD"] = StringCol(64, dflt='NULL')
        patent_attributes_datatypes["SECDLWBD"] = StringCol(64, dflt='NULL')

        patent_table = TableCollection(
            "patent", patent_attributes_datatypes, patent_data_path, target_folder, ",", "PATENT")
        patent_table_model = TableModelCategory(
            "patent", list(patent_attributes_datatypes.keys()), "PATENT")
        patent_collection = CollectionConstructor(
            "patent", patent_table_model, patent_table)

        ## Inventor table

        inventor_attributes_datatypes = dict()
        inventor_attributes_datatypes["PATENT"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["LASTNAM"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["FIRSTNAM"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["MIDNAM"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["MODIFNAM"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["STREET"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["CITY"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["POSTATE"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["COUNTRY"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["ZIP"] = StringCol(64, dflt='NULL')
        inventor_attributes_datatypes["INVSEQ"] = StringCol(64, dflt='NULL')

        inventor_table = TableCollection(
            "inventor", inventor_attributes_datatypes, inventor_data_path, target_folder, ",")
        inventor_table_model = TableModelCategory(
            "inventor", list(inventor_attributes_datatypes.keys()))
        inventor_collection = CollectionConstructor(
            "inventor", inventor_table_model, inventor_table)

        ## Assignee table

        assignee_attributes_datatypes = dict()
        assignee_attributes_datatypes["ASSIGNEE"] = StringCol(64, dflt='NULL')
        assignee_attributes_datatypes["ASSNAME"] = StringCol(64, dflt='NULL')
        assignee_attributes_datatypes["CNAME"] = StringCol(64, dflt='NULL')
        assignee_attributes_datatypes["CUSIP"] = StringCol(64, dflt='NULL')
        assignee_attributes_datatypes["OWN"] = StringCol(64, dflt='NULL')
        assignee_attributes_datatypes["PNAME"] = StringCol(64, dflt='NULL')
        assignee_attributes_datatypes["SNAME"] = StringCol(64, dflt='NULL')

        assignee_table = TableCollection(
            "assignee", assignee_attributes_datatypes, assignee_data_path, target_folder, ",", "ASSIGNEE")
        assignee_table_model = TableModelCategory("assignee", list(
            assignee_attributes_datatypes.keys()), "ASSIGNEE")
        assignee_collection = CollectionConstructor(
            "assignee", assignee_table_model, assignee_table)

        ## Category table

        category_attributes_datatypes = dict()
        category_attributes_datatypes["CAT"] = StringCol(64, dflt='NULL')
        category_attributes_datatypes["SUBCAT"] = StringCol(64, dflt='NULL')
        category_attributes_datatypes["SUBCATNAME"] = StringCol(
            64, dflt='NULL')
        category_attributes_datatypes["CATNAMESHORT"] = StringCol(
            64, dflt='NULL')
        category_attributes_datatypes["CATENAMELONG"] = StringCol(
            64, dflt='NULL')

        category_table = TableCollection(
            "category", category_attributes_datatypes, category_data_path, target_folder, ",", "CAT")
        category_table_model = TableModelCategory(
            "category", list(category_attributes_datatypes.keys()), "CAT")
        category_collection = CollectionConstructor(
            "category", category_table_model, category_table)

        ## Class table

        class_attributes_datatypes = dict()
        class_attributes_datatypes["CLASS"] = StringCol(64, dflt='NULL')
        class_attributes_datatypes["CNAME"] = StringCol(64, dflt='NULL')
        class_attributes_datatypes["SUBCAT"] = StringCol(64, dflt='NULL')
        class_attributes_datatypes["CAT"] = StringCol(64, dflt='NULL')

        class_table = TableCollection(
            "class", class_attributes_datatypes, class_data_path, target_folder, ",", "CLASS")
        class_table_model = TableModelCategory(
            "class", list(class_attributes_datatypes.keys()), "CLASS")
        class_collection = CollectionConstructor(
            "class", class_table_model, class_table)

        ## Citation graph

        edge_info = [{"file_path": citation_data_path, "delimiter": ",", "schema": [
            "CITING", "CITED"], "source_attribute_index": 0, "target_attribute_index": 1}]
        vertex_info = []
        citation_graph_model = GraphModelCategory(
            "citation", ["PATENTID"], ["CITED"])
        citation_graph = GraphCollection(
            "citation", vertex_info, edge_info, target_folder)
        citation_graph_collection = CollectionConstructor(
            "citation", citation_graph_model, citation_graph)

        ## Collect the functors together to form the collection of objects

        objects["patent"] = patent_collection
        objects["inventor"] = inventor_collection
        objects["assignee"] = assignee_collection
        objects["category"] = category_collection
        objects["class"] = class_collection
        objects["citation"] = citation_graph_collection

        morphisms = initialize_patent_morphisms(objects)

        self.patent_multi_model_database = MultiModelDB(
            "Patent multi-model database", objects, morphisms, True)

    def get_multi_model_db(self):
        return self.patent_multi_model_database
