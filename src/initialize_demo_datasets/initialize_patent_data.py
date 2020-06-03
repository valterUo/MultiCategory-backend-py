import os
dirname = os.path.dirname(__file__)
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from instance_category.instance_category import InstanceCategory

def init():
    objects = dict()
    morphisms = dict()

    assignee_data_path = os.path.join(
        dirname, "..\\..\\data\\Patent\\assignee.table")
    category_data_path = os.path.join(
        dirname, "..\\..\\data\\Patent\\category.table")
    citation_data_path = os.path.join(
        dirname, "..\\..\\data\\Patent\\citation.graph")
    class_data_path = os.path.join(
        dirname, "..\\..\\data\\Patent\\class.table")
    inventor_data_path = os.path.join(
        dirname, "..\\..\\data\\Patent\\inventor.table")
    patent_data_path = os.path.join(
        dirname, "..\\..\\data\\Patent\\patent.table")

    # Objects

    patent_table = CollectionObject("patent_table", "relational", "patent", lambda x : x, 
        {"filePath": patent_data_path, "fileformat": "csv", 
            "schema": ["patent","gyear","gdate","appyear","country","postate","assignee","asscode","claims","nclass","cat","subcat","cmade","creceive","ratiocit","general","original","fwdaplag","bckgtlag","selfctub","selfctlb","secdupbd","secdlwbd"], 
            "keyAttribute": "patent", "separator": ","})

    assignee_table = CollectionObject("assignee_table", "relational", "assignee", lambda x : x,
        { "filePath": assignee_data_path, "fileformat": "csv",
            "schema": ["assignee","assname","cname","cusip","own","pname","sname"], "keyAttribute": "assignee", "separator": ",")

    category_table = CollectionObject("category_table", "relational", "category", lambda x : x,
        { "filePath": category_data_path, "fileformat": "csv",
            "schema": ["cat", "subcat", "subcatname", "catnameshort", "catenamelong"], "keyAttribute": "cat", "separator": ",")

    class_table = CollectionObject("class_table", "relational", "class", lambda x : x,
        { "filePath": class_data_path, "fileformat": "csv",
            "schema": ["class", "cname", "subcat", "cat"], "keyAttribute": "class", "separator": ",")

    inventor_table = CollectionObject("inventor_table", "relational", "inventor", lambda x : x,
        { "filePath": inventor_data_path, "fileformat": "csv",
            "schema": ["patent", "lastnam", "firstnam", "midnam", "modifnam", "street", "city", "postate", "country", "zip", "invseq"], "keyAttribute": ["lastnam", "firtsnam", "midnam"], "separator": ",")

