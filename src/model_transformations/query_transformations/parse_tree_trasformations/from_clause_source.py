from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import alias_mapping, set_alias_for_db_name
from external_database_connections.postgresql.postgres import Postgres
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import get_cte_iterator_for_cte_name
rel_db = Postgres("ldbcsf1")


class FromClauseSource:

    """
    One of the collection from the data is queried: table in the database or cte

    rel_alias is a sort of variable that Cypher uses so that we can access attributes in the collection
    """

    def __init__(self, clause, cte_name = ""):
        self.clause = clause
        self.cte_name = cte_name
        self.relname = None
        self.rel_alias = None
        self.in_database = False

        self.range_var = self.clause["RangeVar"]
        self.relname = self.range_var["relname"] #message, cposts
        
        if rel_db.contains_table(self.relname):
            self.in_database = True

        if self.in_database:
            if "alias" in self.range_var.keys():
                self.rel_alias = self.range_var["alias"]["Alias"]["aliasname"]
                set_alias_for_db_name(self.rel_alias, self.relname)
            else:
                self.rel_alias = alias_mapping(self.relname)
        else:
            if "alias" in self.range_var.keys():
                self.rel_alias = self.range_var["alias"]["Alias"]["aliasname"]
                #print(self.rel_alias)
                #set_alias_for_db_name(self.rel_alias, self.relname)
            else:
                self.rel_alias = get_cte_iterator_for_cte_name(self.relname)

    def get_relname(self):
        return self.relname

    def get_rel_alias(self):
        return self.rel_alias

    def get_if_in_database(self):
        return self.in_database

    def transform_into_cypher(self):
        res = ""
        if self.rel_alias and self.relname:
            if self.in_database:
                return "(" + self.rel_alias + " : " + self.relname + ")"
            else:
                return self.relname + " AS " + self.rel_alias
        else:
            print(self.clause)
        return res
