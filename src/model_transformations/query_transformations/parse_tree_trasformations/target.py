from model_transformations.query_transformations.parse_tree_trasformations.column import Column


class Target:

    def __init__(self, target_list, from_clause, cte=False, cte_aliases=[]):
        self.res_target = target_list
        self.from_clause = from_clause
        self.cte = cte
        self.columns = []

        for elem in target_list:
            if "ResTarget" in elem:
                if "val" in elem["ResTarget"]:
                    if "ColumnRef" in elem["ResTarget"]["val"]:
                        self.columns.append(
                            Column(elem["ResTarget"]["val"]["ColumnRef"], self.from_clause))

        if cte_aliases:
            self.cte_aliases = cte_aliases
        else:
            self.cte_aliases = [col.get_alias() for col in self.columns]

    def transform_into_cypher(self):
        if self.cte:
            res = "WITH collect({"
            for i, cte_alias in enumerate(self.cte_aliases):
                res += cte_alias + " : " + \
                    self.columns[i].transform_into_cypher() + ", "
            res = res[0:-2] + "})"
            return res
        else:
            res = ""
            for elem in self.columns:
                res += elem.transform_into_cypher() + ", "
            res = res[0:-2]
            return "RETURN " + res + "\n"
