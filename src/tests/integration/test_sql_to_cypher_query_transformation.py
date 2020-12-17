import glob
import os
import unittest
import os

from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_transformations.parse_tree_trasformations.sql_to_cypher import SqlToCypher
from model_transformations.query_transformations.pgSQL.pgSQL import pgSQL


db = Postgres("ldbcsf1")
dirname = os.path.dirname(__file__)

test_cases = dict()
test_files_path = os.path.join(dirname, "..//..//model_transformations//ldbc//ldbc_sql//*.sql")
filenames = glob.glob(test_files_path)
for i, file_name in enumerate(filenames):
    with open(file_name, 'r') as reader:
        lines = reader.read()
        test_cases[os.path.basename(file_name)] = lines

result_cases = dict()
result_files_path = os.path.join(dirname, "..//..//test_results//sql_to_cypher_automatic//*.cypher")
filenames = glob.glob(result_files_path)
for i, file_name in enumerate(filenames):
    with open(file_name, 'r') as reader:
        lines = reader.read()
        result_cases[os.path.basename(file_name)] = lines

def clean(s):
    return s.replace("\n", " ").replace(" ", "").lower()

def general_preparation(file_name):
    query = test_cases[file_name +".sql"]
    parse_tree = pgSQL(query).get_parse_tree()
    res = SqlToCypher(parse_tree).transform_into_cypher()
    real = clean(result_cases[file_name + ".cypher"])
    return clean(res), real

class TestSQLtoCypher(unittest.TestCase):

    def test_short_1(self):
        file_name = "interactive-short-1"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

    def test_short_2(self):
        file_name = "interactive-short-2"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

    def test_short_3(self):
        file_name = "interactive-short-3"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

    def test_short_4(self):
        file_name = "interactive-short-4"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

    def test_bi1(self):
        file_name = "bi-1"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

    def test_bi2(self):
        file_name = "bi-2"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

    def test_bi10(self):
        file_name = "bi-10"
        res, real = general_preparation(file_name)
        self.assertEqual(res, real)

if __name__ == '__main__':
    unittest.main()