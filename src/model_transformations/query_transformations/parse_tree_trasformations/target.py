from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import get_cte_column_names_for_cte_name


class Target:

    def __init__(self, target_list, from_clause, cte = False, cte_name = ""):
        self.res_target = target_list
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.columns = []

        for elem in target_list:
            if "ResTarget" in elem:
                rename = None
                if "name" in elem["ResTarget"]:
                    rename = elem["ResTarget"]["name"]
                if "val" in elem["ResTarget"]:
                    if "ColumnRef" in elem["ResTarget"]["val"]:
                        self.columns.append(
                            Column(elem["ResTarget"]["val"]["ColumnRef"], self.from_clause, self.cte, self.cte_name, rename))


    def transform_into_cypher(self):
        if self.cte:
            try:
                cte_column_names = get_cte_column_names_for_cte_name(self.cte_name)
            except:
                cte_column_names = [elem.get_name() for elem in self.columns]

            res = "WITH collect({"

            for i, cte_column_alias in enumerate(cte_column_names):
                res += cte_column_alias + " : " + self.columns[i].transform_into_cypher() + ", "

            res = res[0:-2] + "})"

            # if self.cte_name != "":
            #     res += " AS " + self.cte_name

            return res

        else:
            res = ""
            for elem in self.columns:
                res += elem.transform_into_cypher() + ", "
            res = res[0:-2]
            return "RETURN " + res
