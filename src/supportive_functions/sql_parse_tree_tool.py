"""
This file implements script to create parse multiple SQL queries into their parse tree format.
"""

from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL
import json
import os
import glob

target_dictory = "C://Users//Valter Uotila//Desktop//parsed_ldbc_queries//"
dirname = os.path.dirname(__file__)
example_files_path = os.path.join(dirname, "..//model_transformations//ldbc//ldbc_sql//*.sql")
example_filenames = glob.glob(example_files_path)
for file_name in example_filenames:
      print(file_name)
      with open(file_name, 'r') as reader:
            lines = reader.read()
            parse_tree = pgSQL(lines).get_parse_tree()
            print(len(parse_tree))
            with open(target_dictory + os.path.basename(file_name) + ".json", "w+") as json_file:
                  json.dump(parse_tree, json_file)