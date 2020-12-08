from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import alias_mapping, set_alias_for_db_name
from external_database_connections.postgresql.postgres import Postgres
rel_db = Postgres("ldbcsf1")


class FromClauseSource:

    """
    The instance of this class is uniquely defined by relname attribute.
    """

    def __init__(self, clause):
        self.clause = clause
        self.range_var = None
        self.relname = None
        self.location = None
        self.relpersistence = None
        self.aliasname = None
        self.in_database = False

        self.range_var = self.clause["RangeVar"]
        self.location = self.range_var["location"]
        self.relpersistence = self.range_var["relpersistence"]
        self.relname = self.range_var["relname"]
        if rel_db.contains_table(self.relname):
            self.in_database = True

        if "alias" in self.range_var.keys():
            self.aliasname = self.range_var["alias"]["Alias"]["aliasname"]
            set_alias_for_db_name(self.aliasname, self.relname)
        else:
            self.aliasname = alias_mapping(self.relname)

    def get_relname(self):
        return self.relname

    def get_aliasname(self):
        return self.aliasname

    def get_if_in_database(self):
        return self.in_database

    def transform_into_cypher(self):
        res = ""
        if self.aliasname and self.relname:
            if self.in_database:
                return "(" + self.aliasname + " : " + self.relname + ")"
            else:
                return self.relname + " AS " + self.aliasname
        else:
            print(self.clause)
        return res
