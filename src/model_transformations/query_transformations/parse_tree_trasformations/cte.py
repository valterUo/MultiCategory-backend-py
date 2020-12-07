from model_transformations.query_transformations.parse_tree_trasformations.cte_column_mapping import set_column_names_for_cte, set_cte_for_column_name
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt


class CommonTableExpr:

    def __init__(self, raw_cte):
        #print(json.dumps(raw_cte, indent=2))
        self.raw_cte = raw_cte
        self.aliascolnames = [name["String"]["str"]
                              for name in raw_cte["aliascolnames"]]
        self.ctename = raw_cte["ctename"]
        set_column_names_for_cte(self.ctename, self.aliascolnames)
        for column_name in self.aliascolnames:
            set_cte_for_column_name(column_name, self.ctename)
        self.ctequery = SelectStmt(
            raw_cte["ctequery"]["SelectStmt"], cte=True, cte_aliases=self.aliascolnames)
        self.location = raw_cte["location"]

    def transform_into_cypher(self):
        return self.ctequery.transform_into_cypher()[0:-1] + " AS " + self.ctename + "\n"
