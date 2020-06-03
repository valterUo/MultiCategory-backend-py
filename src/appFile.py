from functools import reduce
import networkx as nx
import json
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from instance_category.objects.collection_object import CollectionObject
from instance_category.morphisms.morphism import Morphism
from multi_model_join.join import add_to_dict, join, join_relational_xml
from multi_model_join.graph_join.graph_join import join_graph_graph, join_graph_relational
import initialize_demo_datasets.initialize_ecommerce as commerce
from instance_functor.instance_functor import InstanceFunctor
import pickle
import csv
import mmap
from io import StringIO

patent_table = CollectionObject("patent_table", "relational", "patent", lambda x : x, 
        {"filePath": "C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\Patent\\patent.table", "fileformat": "csv", 
            "schema": ["patent","gyear","gdate","appyear","country","postate","assignee","asscode","claims","nclass","cat","subcat","cmade","creceive","ratiocit","general","original","fwdaplag","bckgtlag","selfctub","selfctlb","secdupbd","secdlwbd"], 
            "keyAttribute": "patent", "separator": ","})

# with open("C:\\Users\\Valter Uotila\\Desktop\\MultiCategory-backend-py\\data\\Patent\\patent.pyc", "rb") as db_file:
#     dictionary = pickle.load(db_file)

# print(dictionary["3070856"])

