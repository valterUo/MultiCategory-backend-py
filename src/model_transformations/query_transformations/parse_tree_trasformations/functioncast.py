import json

from model_transformations.query_transformations.parse_tree_trasformations.column import Column


def pg_functions_to_neo4j_functions(funcCall, from_clause, cte, cte_name, rename):
    func_name = funcCall["funcname"][-1]["String"]["str"]
    args = funcCall["args"]
    fields = []
    func_type = None
    for elem in args:
        if "ColumnRef" in elem.keys():
            col = Column(elem["ColumnRef"], from_clause, cte, cte_name, rename)
            fields.append(col)
        elif "A_Const" in elem.keys():
            func_type = elem["A_Const"]["val"]["String"]["str"]
        elif "A_Expr" in elem.keys():
            from model_transformations.query_transformations.parse_tree_trasformations.aexpression import AExpression
            a_expr = AExpression(elem["A_Expr"]["lexpr"], elem["A_Expr"]["name"][0]["String"]
                                 ["str"], elem["A_Expr"]["rexpr"], from_clause, cte, cte_name, rename)
            fields.append(a_expr)
    if func_name == "date_part":
        print(func_type)
        return {"fields": fields, "func": {"pre": "datetime(", "post": ")." + func_type}}
    elif func_name == "avg":
        return {"fields": fields, "func": {"pre": "avg(", "post": ")"}}
    elif func_name == "count":
        return {"fields": fields, "func": {"pre": "count(", "post": ")"}}
    elif func_name == "sum":
        return {"fields": fields, "func": {"pre": "sum(", "post": ")"}}
    elif func_name == "abs":
        return {"fields": fields, "func": {"pre": "abs(", "post": ")"}}
