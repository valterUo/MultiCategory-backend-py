from model_transformations.query_transformations.parse_tree_trasformations.column import Column
from model_transformations.query_transformations.parse_tree_trasformations.functioncast import pg_functions_to_neo4j_functions


class FuncCall:

    def __init__(self, func_call, from_clause, cte, cte_name, rename, index = 0):
        self.func_call = func_call
        self.from_clause = from_clause
        self.cte = cte
        self.cte_name = cte_name
        self.rename = rename
        self.col_refer = None
        self.func = None
        self.index = index

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
                print("Not implemented yet")
        elif func_name == "avg":
            call = pg_functions_to_neo4j_functions(self.func_call)
            func_column = Column(
                {"fields": [{"String": {"str": call["field"]}}]}, self.from_clause, self.cte, self.cte_name, accept_collection_alias=True)
            self.func = "avg(" + \
                func_column.transform_into_cypher() + ")"
            self.col_refer = Column(
                {"fields": [{"String": {"str": "a" + str(self.index)}}]}, self.from_clause, self.cte, self.cte_name, rename=self.rename, accept_collection_alias=False)
        elif func_name == "sum":
            call = pg_functions_to_neo4j_functions(
                self.func_call)
            func_column = Column(
                {"fields": [{"String": {"str": call["field"]}}]}, self.from_clause, self.cte, self.cte_name, accept_collection_alias=True)
            self.func = "sum(" + \
                func_column.transform_into_cypher() + ")"
            self.col_refer = Column(
                {"fields": [{"String": {"str": "s" + str(self.index)}}]}, self.from_clause, self.cte, self.cte_name, rename=self.rename, accept_collection_alias=False)
        else:
            call = pg_functions_to_neo4j_functions(
                self.func_call)
            self.col_refer = Column(
                {"fields": [{"String": {"str": call["field"]}}]}, self.from_clause, self.cte, self.cte_name, self.rename, call["func"])

    def transform_into_cypher(self, with_with=True):
        res = ""
        if self.func:
            if with_with:
                res += "WITH *, "
            res += self.func
            if with_with:
                res += " AS " + self.col_refer.get_field()
        return res

    def get_col_refer(self):
        return self.col_refer
