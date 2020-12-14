from model_transformations.query_transformations.parse_tree_trasformations.alias_mapping import alias_mapping
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import append_cte_table_data
from model_transformations.query_transformations.parse_tree_trasformations.select_stmt import SelectStmt


class CommonTableExpr:

    def __init__(self, raw_cte, index):
        self.raw_cte = raw_cte

        try:
            self.cte_column_names = [name["String"]["str"]
                                 for name in self.raw_cte["aliascolnames"]]
        except KeyError:
            self.cte_column_names = []

        self.ctename = self.raw_cte["ctename"]

        append_cte_table_data(self.ctename, alias_mapping(
            self.ctename), self.cte_column_names, "x" + str(index))

        self.ctequery = SelectStmt(self.raw_cte["ctequery"]["SelectStmt"],
                                   name=self.ctename,
                                   cte=True)

    def transform_into_cypher(self):
        return self.ctequery.transform_into_cypher()
