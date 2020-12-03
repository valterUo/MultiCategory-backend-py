import json
from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import alias_mapping, set_alias_for_db_name


class FromClauseSource:

    """
    The instance of this class is uniquely defined by relname attribute.
    """

    def __init__(self, range_var):
        self.range_var = range_var["RangeVar"]
        self.relname = self.range_var["relname"]
        try:
            self.inh = self.range_var["inh"]
        except KeyError:
            print("Warning: key 'inh' is not present in the parse tree")
        try:
            self.location = self.range_var["location"]
        except KeyError:
            print("Warning: key 'location' is not present in the parse tree")
        try:
            self.relpersistence = self.range_var["relpersistence"]
        except KeyError:
            print("Warning: key 'relpersistence' is not present in the parse tree")
        if "alias" in self.range_var.keys():
            self.aliasname = self.range_var["alias"]["Alias"]["aliasname"]
            set_alias_for_db_name(self.aliasname, self.relname)
        else:
            self.aliasname = alias_mapping(self.relname)

    def get_relname(self):
        return self.relname

    def get_aliasname(self):
        return self.aliasname

    def transform_into_cypher(self):
        return "(" + self.aliasname + " : " + self.relname + ")"
