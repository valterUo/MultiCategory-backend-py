def pg_functions_to_neo4j_functions(funcCall):
    #print(funcCall)
    func_name = funcCall["funcname"][-1]["String"]["str"]
    args = funcCall["args"]
    fields = None
    func_type = None
    for elem in args:
        if "ColumnRef" in elem.keys():
            fields = elem["ColumnRef"]["fields"]
        elif "A_Const" in elem.keys():
            func_type = elem["A_Const"]["val"]["String"]["str"]
    if func_name == "date_part":
        return {"fields": fields, "func": {"pre": "datetime(", "post": ")." + func_type}}
    elif func_name == "avg":
        return {"fields": fields, "func": {"pre": "avg(", "post": ")"}}
    elif func_name == "count":
        return {"fields": fields, "func": {"pre": "count(", "post": ")"}}
    elif func_name == "sum":
        return {"fields": fields, "func": {"pre": "sum(", "post": ")"}}