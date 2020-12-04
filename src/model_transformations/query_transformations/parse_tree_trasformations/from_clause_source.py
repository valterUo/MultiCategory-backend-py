import json
from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import alias_mapping, set_alias_for_db_name
from model_transformations.query_transformations.parse_tree_trasformations.join import Join


class FromClauseSource:

    """
    The instance of this class is uniquely defined by relname attribute.
    """

    def __init__(self, clause):
        self.range_var = None
        self.relname = None
        self.inh = None
        self.location = None
        self.relpersistence = None
        self.aliasname = None
        self.join_expr = None

        if "RangeVar" in clause.keys():

            self.range_var = clause["RangeVar"]
            self.relname = self.range_var["relname"]
            self.inh = self.range_var["inh"]
            self.location = self.range_var["location"]
            self.relpersistence = self.range_var["relpersistence"]

            if "alias" in self.range_var.keys():
                self.aliasname = self.range_var["alias"]["Alias"]["aliasname"]
                set_alias_for_db_name(self.aliasname, self.relname)
            else:
                self.aliasname = alias_mapping(self.relname)

        elif "JoinExpr" in clause.keys():

            self.join_expr = Join(clause["JoinExpr"])

    def get_relname(self):
        return self.relname

    def get_aliasname(self):
        return self.aliasname

    def transform_into_cypher(self):
        if self.aliasname and self.relname:
            return "(" + self.aliasname + " : " + self.relname + ")"
        return ""
