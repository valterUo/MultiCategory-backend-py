from model_transformations.query_transformations.parse_tree_trasformations.column import Column


class Sort:

    def __init__(self, sort_clause, cte = False, from_clause = None, cte_name = ""):
        self.sort_clause = sort_clause
        self.cte = cte
        self.from_clause = from_clause
        self.order_by = []
        self.cte_name = cte_name
        self.modes = []

        for elem in self.sort_clause:
            if elem["SortBy"]["sortby_dir"] == 2:
                self.modes.append("DESC")
            else:
                self.modes.append("ASC")

            self.order_by.append(Column(elem["SortBy"]["node"]["ColumnRef"], self.from_clause, self.cte, self.cte_name))

    def transform_into_cypher(self):
        res = ""
        if self.cte:
            res = "WITH *,"
            for elem in self.order_by:
                res += elem.get_collection_alias() + ", "
            res = res[0:-2] + "\n"
        res += "ORDER BY "
        for i, elem in enumerate(self.order_by):
            res += elem.transform_into_cypher() + " " + self.modes[i] + ", "
        res = res[0:-2] + "\n"
        return res