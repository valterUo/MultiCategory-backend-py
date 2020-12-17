from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.functioncast import pg_functions_to_neo4j_functions


class FuncCall:

    def __init__(self, func_call, from_clause, cte, cte_name, rename, index=0):
        self.func_call = func_call
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.rename = rename
        self.col_refer = None
        self.func = None
        self.index = index
        self.distinct = False

        if "agg_distinct" in self.func_call:
            self.distinct = self.func_call["agg_distinct"]

        func_name = self.func_call["funcname"][-1]["String"]["str"]

        if func_name == "count":
            star = False
            if "agg_star" in self.func_call:
                star = self.func_call["agg_star"]
            if star:
                self.func = "count(*)"
                self. col_refer = Column({"fields": [
                                         {"String": {"str": "c" + str(self.index)}}]},  self.from_clause, self.cte, self.cte_name, rename=self.rename, accept_collection_alias=False)
            else:
                for elem in self.func_call["args"]:
                    if "CaseExpr" in elem:
                        from model_transformations.query_transformations.parse_tree_trasformations.case_expression import CaseExpression
                        case_expr = CaseExpression(
                            elem["CaseExpr"], self.from_clause, self.cte, self.cte_name, self.rename)
                        if self.distinct:
                            self.func = "count(distinct " + \
                                case_expr.transform_into_cypher() + ")"
                        else:
                            self.func = "count( " + \
                                case_expr.transform_into_cypher() + ")"
                        self. col_refer = Column({"fields": [
                            {"String": {"str": "c" + str(self.index)}}]},  self.from_clause, self.cte, self.cte_name, rename=self.rename, accept_collection_alias=False)

        # elif func_name == "avg":
        #     call = pg_functions_to_neo4j_functions(self.func_call, self.from_clause, self.cte, self.cte_name, self.rename,)
        #     func_column = Column(
        #         {"fields": call["fields"]}, self.from_clause, self.cte, self.cte_name, accept_collection_alias=True)
        #     self.func = "avg(" + \
        #         func_column.transform_into_cypher() + ")"
        #     self.col_refer = Column(
        #         {"fields": [{"String": {"str": "a" + str(self.index)}}]}, self.from_clause, self.cte, self.cte_name, self.rename, accept_collection_alias=False)
        # elif func_name == "sum":
        #     call = pg_functions_to_neo4j_functions(
        #         self.func_call, self.from_clause, self.cte, self.cte_name, self.rename,)
        #     func_column = Column(
        #         {"fields": call["fields"]}, self.from_clause, self.cte, self.cte_name, accept_collection_alias=True)
        #     self.func = "sum(" + \
        #         func_column.transform_into_cypher() + ")"
        #     self.col_refer = Column(
        #         {"fields": [{"String": {"str": "s" + str(self.index)}}]}, self.from_clause, self.cte, self.cte_name, rename=self.rename, accept_collection_alias=False)
        else:
            call = pg_functions_to_neo4j_functions(
                self.func_call, self.from_clause, self.cte, self.cte_name, self.rename,)
            # print(call["fields"])
            # print(call["func"])
            for elem in call["fields"]:
                self.func = call["func"]["pre"] + elem.transform_into_cypher(False) + call["func"]["post"]
            self.col_refer = Column(
                {"fields": [{"String": {"str": "func" + str(self.index)}}]}, self.from_clause, self.cte, self.cte_name, self.rename, accept_collection_alias=False)
            # func = Column(
            #     {"fields": call["fields"]}, self.from_clause, self.cte, self.cte_name, self.rename, call["func"])
            # self.func = func.transform_into_cypher()
            # self.col_refer = Column(
            #     {"fields": call["fields"]}, self.from_clause, self.cte, self.cte_name, self.rename, call["func"])

    def transform_into_cypher(self, with_with=True):
        res = ""
        if self.func:
            if with_with:
                res += "WITH *, "
            res += self.func
            if with_with and self.col_refer:
                res += " AS " + self.col_refer.get_field()
        return res

    def get_col_refer(self):
        return self.col_refer
