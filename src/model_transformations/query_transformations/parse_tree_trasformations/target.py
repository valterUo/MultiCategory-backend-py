from model_transformations.query_transformations.parse_tree_trasformations.column import Column


class Target:

    def __init__(self, target_list, from_clause):
        self.res_target = target_list
        self.from_clause = from_clause
        self.columns = []

        for elem in target_list:
            if "ResTarget" in elem:
                if "val" in elem["ResTarget"]:
                    if "ColumnRef" in elem["ResTarget"]["val"]:
                        self.columns.append(
                            Column(elem["ResTarget"]["val"]["ColumnRef"], self.from_clause))

    def transform_into_cypher(self):
        res = ""
        for elem in self.columns:
            res += elem.transform_into_cypher() + ", "
        res = res[0:-2]
        return "RETURN " + res + "\n"
