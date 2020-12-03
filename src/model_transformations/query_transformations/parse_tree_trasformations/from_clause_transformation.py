from typing import OrderedDict
from model_transformations.query_transformations.parse_tree_trasformations.from_clause_source import FromClauseSource


class FromClause:

    def __init__(self, from_clause):
        self.from_clause = from_clause
        self.sources = []
        if type(self.from_clause) == list:
            for elem in self.from_clause:
                self.sources.append(FromClauseSource(elem))
    
    def get_sources(self):
        return self.sources

    def transform_into_cypher(self):
        res = ""
        for elem in self.sources:
            res += elem.transform_into_cypher() + ", "
        res = res[0:-2]
        return "MATCH " + res + "\n"