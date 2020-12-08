from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import get_alias_for_name
from model_transformations.query_transformations.parse_tree_trasformations.cte_column_mapping import column_names_to_cte_names_mapping

rel_db = Postgres("ldbcsf1")

class Column:

    def __init__(self, column_ref, from_clause = None):
        self.column_ref = column_ref
        self.fields = self.column_ref["fields"]
        self.from_clause = from_clause
        self.field = None
        self.alias = None

        try:
            self.location = self.column_ref["location"]
        except KeyError:
            print("Target does not have 'location' key")

        if len(self.fields) == 2:
            self.alias = self.fields[0]["String"]["str"]
            self.field = self.fields[1]["String"]["str"]
        elif len(self.fields) == 1:
            raw_field = self.fields[0]
            if "String" in raw_field.keys():
                if "str" in raw_field["String"]:
                    self.field = raw_field["String"]["str"]
                    table_name = rel_db.get_table_for_attribute(self.field)
                    if table_name == None:
                        table_name = column_names_to_cte_names_mapping(self.field)
                    self.alias = get_alias_for_name(table_name)
        else:
            print("Too many or none fields or what?")
        
    def transform_into_cypher(self, alias_mapping = {}):
        if len(alias_mapping) > 0:
            if self.alias in alias_mapping.keys():
                return alias_mapping[self.alias] + "." + self.field
        return self.alias + "." + self.field

    def get_alias(self):
        return self.alias

    def get_field(self):
        return self.field
