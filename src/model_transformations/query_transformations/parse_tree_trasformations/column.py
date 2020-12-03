from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import get_alias_for_name

rel_db = Postgres("ldbcsf1")

class Column:

    def __init__(self, column_ref, from_clause):
        self.column_ref = column_ref
        self.from_clause = from_clause
        self.field = None
        self.alias = None

        try:
            self.location = column_ref["location"]
        except KeyError:
            print("Target does not have 'location' key")

        if len(column_ref["fields"]) > 1:
            print("Multiple fields?")
        else:
            elem = column_ref["fields"][0]
            if "String" in elem.keys():
                if "str" in elem["String"]:
                    self.field = elem["String"]["str"]
                    table_name = rel_db.get_table_for_attribute(self.field)
                    self.alias = get_alias_for_name(table_name)
        
    def transform_into_cypher(self):
        return self.alias + "." + self.field
