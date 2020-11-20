from model_transformations.query_transformations.SQL.sql import SQL


class SUBQUERY:

    def __init__(self, name, query_string, rel_db):
        self.name = name
        self.query_string = query_string
        self.db = rel_db
        self.query = SQL(self.name, self.query_string, self.db)
    
    def get_subquery(self):
        return self.query

    def get_subquery_string(self):
        return self.query.get_cypher()