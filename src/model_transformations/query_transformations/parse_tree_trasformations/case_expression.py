from model_transformations.query_transformations.parse_tree_trasformations.aexpression import AExpression
import json

from model_transformations.query_transformations.parse_tree_trasformations.column import Column


class CaseWhen:

    def __init__(self, case_when, from_clause, cte, cte_name, rename):
        #print(json.dumps(case_when, indent=2))
        self.case_when = case_when
        self.expr = None
        self.result = None

        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.rename = rename

        if "A_Expr" in self.case_when["expr"]:
            temp_case = self.case_when["expr"]["A_Expr"]
            left = temp_case["lexpr"]
            right = temp_case["rexpr"]
            operator = temp_case["name"][0]["String"]["str"]
            self.expr = AExpression(
                left, operator, right, self.from_clause, self.cte, self.cte_name, self.rename)

        if "A_Const" in self.case_when["result"]:
            temp_case = self.case_when["result"]["A_Const"]["val"]
            if "Integer" in temp_case:
                self.result = temp_case["Integer"]["ival"]
            elif "String" in temp_case:
                self.result = temp_case["String"]["str"]
            elif "Float" in temp_case:
                self.result = temp_case["Float"]["str"]
            elif "Null" in temp_case:
                self.result = "NULL"
        elif "ColumnRef" in self.case_when["result"]:
            col = Column(self.case_when["result"]["ColumnRef"],
                         self.from_clause, self.cte, self.cte_name, self.rename)
            self.result = col.transform_into_cypher()

    def transform_into_cypher(self):
        return "WHEN " + self.expr.transform_into_cypher(with_with=False) + " THEN " + str(self.result)


class CaseExpression:

    def __init__(self, case_expr, from_clause, cte, cte_name, rename):
        self.initial_case_expr = case_expr
        self.expressions = []
        self.default = None

        self.rename = rename
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name

        temp_initial = self.initial_case_expr["defresult"]["A_Const"]["val"]

        if "Integer" in temp_initial.keys():
            self.default = temp_initial["Integer"]["ival"]
        elif "String" in temp_initial.keys():
            self.default = temp_initial["String"]["str"]
        elif "Float" in temp_initial.keys():
            self.default = temp_initial["Float"]["str"]
        elif "Null" in temp_initial.keys():
            self.default = "NULL"

        for elem in self.initial_case_expr["args"]:
            self.expressions.append(CaseWhen(
                elem["CaseWhen"], self.from_clause, self.cte, self.cte_name, self.rename))

    def get_name(self):
        return self.rename

    def transform_into_cypher(self):
        res = ""
        res += "CASE \n"
        for expr in self.expressions:
            res += expr.transform_into_cypher() + "\n"
        res += "ELSE " + str(self.default) + "\n"
        res += "END"
        return res
