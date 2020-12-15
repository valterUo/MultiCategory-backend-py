from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import alias_mapping
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import append_cte_table_data
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt


class CommonTableExpr:

    def __init__(self, raw_cte, index):
        self.raw_cte = raw_cte
        self.ctename = self.raw_cte["ctename"]
        self.aliasname = "x" + str(index)

        try:
            self.cte_column_names = [name["String"]["str"]
                                 for name in self.raw_cte["aliascolnames"]]
        except KeyError:
            # If there are no explicit cte column names, then they need to be parsed from the targetlist
            self.cte_column_names = self.search_cte_column_names()

        append_cte_table_data(self.ctename, alias_mapping(
            self.ctename), self.cte_column_names, self.aliasname)

        self.ctequery = SelectStmt(self.raw_cte["ctequery"]["SelectStmt"],
                                   name=self.ctename,
                                   cte=True)

    def transform_into_cypher(self):
        return self.ctequery.transform_into_cypher()

    def search_cte_column_names(self):
        res = []
        for elem in self.raw_cte["ctequery"]["SelectStmt"]["targetList"]:
            if "name" in elem["ResTarget"]:
                res.append(elem["ResTarget"]["name"])
            else:
                if "ColumnRef" in elem["ResTarget"]["val"]:
                    name = elem["ResTarget"]["val"]["ColumnRef"]["fields"][0]["String"]["str"]
                    res.append(name)
                else:
                    print("CTE column name not found!")
        return res

