from model_transformations.query_transformations.parse_tree_trasformations.aexpression import AExpression
from model_transformations.query_transformations.parse_tree_trasformations.case_expression import CaseExpression
from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.cte_table_data import get_cte_column_names_for_cte_name
from model_transformations.query_transformations.parse_tree_trasformations.func_call import FuncCall


class Target:

    def __init__(self, target_list, from_clause, cte=False, cte_name=""):
        self.res_target = target_list
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.columns = []
        self.functions = []
        self.aexpressions = []

        for i, elem in enumerate(target_list):
            if "ResTarget" in elem:
                rename = None
                if "name" in elem["ResTarget"]:
                    rename = elem["ResTarget"]["name"]
                if "val" in elem["ResTarget"]:
                    temp_val = elem["ResTarget"]["val"]
                    if "ColumnRef" in temp_val:
                        col = Column(temp_val["ColumnRef"], self.from_clause, self.cte, self.cte_name, rename)
                        self.columns.append(col)
                    elif "FuncCall" in temp_val:
                        func = FuncCall(temp_val["FuncCall"], self.from_clause, self.cte, self.cte_name, rename, i)
                        col_refer = func.get_col_refer()
                        self.columns.append(col_refer)
                        self.functions.append(func)
                    elif "A_Expr" in temp_val:
                        left = temp_val["A_Expr"]["lexpr"]
                        right = temp_val["A_Expr"]["rexpr"]
                        operator = temp_val["A_Expr"]["name"][0]["String"]["str"]
                        a_expr = AExpression(left, operator, right, self.from_clause, self.cte, self.cte_name, rename)
                        col_refer = a_expr.get_col_refer()
                        self.columns.append(col_refer)
                        self.aexpressions.append(a_expr)
                    elif "CaseExpr" in temp_val:
                        case_expr = CaseExpression(temp_val["CaseExpr"], self.from_clause, self.cte, self.cte_name, rename)
                        self.columns.append(case_expr)


    def transform_into_cypher(self):
        res = ""
        for elem in self.functions:
            res += elem.transform_into_cypher() + "\n"
        for elem in self.aexpressions:
            res += elem.transform_into_cypher() + "\n"

        if self.cte:
            cte_column_names = [elem.get_name() for elem in self.columns]

            res += "WITH *, collect({"

            for i, cte_column_alias in enumerate(cte_column_names):
                res += cte_column_alias + " : " + \
                    self.columns[i].transform_into_cypher() + ", "

            res = res[0:-2] + "})"

        else:
            res += "RETURN "
            for elem in self.columns:
                res += elem.transform_into_cypher() + ", "
            res = res[0:-2]
        return res
