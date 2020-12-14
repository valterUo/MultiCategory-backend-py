import json
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import get_cte_iterator_for_cte_column_name, get_cte_iterator_for_cte_name, is_cte

rel_db = Postgres("ldbcsf1")


class Column:

    def __init__(self, column_ref = None, from_clause=None, cte=False, cte_name="", rename=None, func = None, accept_collection_alias = True):
        #print(json.dumps(column_ref, indent = 2))
        self.column_ref = column_ref
        self.fields = self.column_ref["fields"]
        self.from_clause = from_clause
        self.field = self.fields[-1]["String"]["str"]
        self.collection_alias = None
        self.cte = cte
        self.cte_name = cte_name
        self.rename = rename
        self.func = func
        self.accept_collection_alias = accept_collection_alias

        if self.accept_collection_alias:
            if len(self.fields) == 2:
                self.collection_alias = self.fields[0]["String"]["str"]
                # Assure that the collection alias is not refering to cte:
                if is_cte(self.collection_alias):
                    self.collection_alias = get_cte_iterator_for_cte_name(
                        self.collection_alias)
            elif len(self.fields) == 1:
                self.find_correct_collection_alias()

    def transform_into_cypher(self):
        if not self.cte:
            if self.rename:
                if self.collection_alias:
                    return self.apply_func(self.collection_alias + "." + self.field) + " AS " + self.rename
                else:
                    return self.apply_func(self.field) + " AS " + self.rename
        if self.collection_alias:
            return self.apply_func(self.collection_alias + "." + self.field)
        else:
            return self.apply_func(self.field)

    def get_collection_alias(self):
        return self.collection_alias

    def get_field(self):
        return self.field
    
    def get_name(self):
        if self.rename:
            return self.rename
        return self.field

    def set_collection_alias(self, alias):
        self.collection_alias = alias

    def set_field(self, field):
        self.field = field

    def set_name(self, name):
        self.rename = name

    def set_func(self, func):
        self.func = func

    def find_correct_collection_alias(self):
        if not self.collection_alias:
            table_name = rel_db.get_table_for_attribute(self.field)
            if table_name in self.from_clause.get_relnames():
                self.collection_alias = self.from_clause.get_alias_for_relname(
                    table_name)

        if not self.collection_alias:
            iterator = get_cte_iterator_for_cte_column_name(self.field)
            if iterator:
                self.collection_alias = iterator

    def apply_func(self, value):
        if self.func != None:
            return self.func["pre"] + value + self.func["post"]
        return value
