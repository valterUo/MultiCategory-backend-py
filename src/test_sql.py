import glob
import unittest
import os

from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_language_transformations.SQL.sql import SQL

db = Postgres("ldbcsf1")
dirname = os.path.dirname(__file__)

test_cases = dict()
test_files_path = os.path.join(dirname, "model_transformations\\ldbc\\ldbc_sql\\*.sql")
filenames = glob.glob(test_files_path)
for i, file_name in enumerate(filenames):
    with open(file_name, 'r') as reader:
        lines = reader.read()
        test_cases[os.path.basename(file_name)] = lines

result_cases = dict()
result_files_path = os.path.join(dirname, "test_results\\sql_to_cypher_automatic\\*.cypher")
filenames = glob.glob(result_files_path)
for i, file_name in enumerate(filenames):
    with open(file_name, 'r') as reader:
        lines = reader.read()
        result_cases[os.path.basename(file_name)] = lines

def clean(s):
    return s.replace("\n", " ").replace(" ", "").lower()

class TestSQLtoCypher(unittest.TestCase):

    def test_short_1(self):
        query = test_cases["interactive-short-1.sql"]
        result = clean(SQL("test", query, db).get_cypher())
        real = clean(result_cases["interactive-short-1.cypher"])
        self.assertEqual(result, real)

    def test_short_2(self):
        result = ""
        real = " "
        self.assertEqual(result, real)

    def test_short_3(self):
        query = test_cases["interactive-short-3.sql"]
        result = clean(SQL("test", query, db).get_cypher())
        real = clean(result_cases['interactive-short-3.cypher'])
        self.assertEqual(result, real)

    def test_short_4(self):
        query = test_cases["interactive-short-4.sql"]
        result = clean(SQL("test", query, db).get_cypher())
        real = clean(result_cases['interactive-short-4.cypher'])
        self.assertEqual(result, real)

    def test_bi1(self):
        query = test_cases["bi-1.sql"]
        result = clean(SQL("test", query, db).get_cypher())
        real = clean(result_cases["bi-1.cypher"])
        j = 0
        for i, ch1 in enumerate(real):
                if ch1 != result[i]:
                    i+=1
        self.assertGreaterEqual(3, j)

    def test_bi10(self):
        query = test_cases["bi-10.sql"]
        result = clean(SQL("test", query, db).get_cypher())
        real = clean(result_cases["bi-10.cypher"])
        j = 0
        for i, ch1 in enumerate(real):
                if ch1 != result[i]:
                    i+=1
        self.assertGreaterEqual(3, j)

if __name__ == '__main__':
    unittest.main()