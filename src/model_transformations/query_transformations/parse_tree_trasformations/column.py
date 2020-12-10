from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import get_cte_iterator_for_cte_column_name, get_cte_iterator_for_cte_name, is_cte

rel_db = Postgres("ldbcsf1")


class Column:

    def __init__(self, column_ref, from_clause=None, cte=False, cte_name="", rename = None):
        self.column_ref = column_ref
        self.fields = self.column_ref["fields"]
        self.from_clause = from_clause
        self.field = None
        self.collection_alias = None
        self.cte = cte
        self.cte_name = cte_name
        self.rename = rename
        
        if self.from_clause:
            print(self.from_clause.get_relnames())

        if len(self.fields) == 2:
            self.collection_alias = self.fields[0]["String"]["str"]
            # Assure that the collection alias is not refering to cte:
            if is_cte(self.collection_alias):
                self.collection_alias = get_cte_iterator_for_cte_name(self.collection_alias)
            self.field = self.fields[1]["String"]["str"]
        elif len(self.fields) == 1:
            self.field = self.fields[0]["String"]["str"]
            self.find_correct_collection_alias()

    def transform_into_cypher(self):
        if not self.cte:
            if self.rename:
                return self.collection_alias + "." + self.field + " AS " + self.rename
        return self.collection_alias + "." + self.field

    def get_collection_alias(self):
        return self.collection_alias

    def get_field(self):
        return self.field

    def get_name(self):
        if self.rename:
            return self.rename
        return self.field

    def find_correct_collection_alias(self):
        if not self.collection_alias:
            table_name = rel_db.get_table_for_attribute(self.field)
            if table_name in self.from_clause.get_relnames():
                self.collection_alias = self.from_clause.get_alias_for_relname(
                    table_name)

        if not self.collection_alias:
            #get_iterator_from_cte_name(self.left_alias)
            iterator = get_cte_iterator_for_cte_column_name(self.field)
            if iterator:
                self.collection_alias = iterator
