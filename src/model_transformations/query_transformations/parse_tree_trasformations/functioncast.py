def pg_functions_to_neo4j_functions(funcCall):
    #print(funcCall)
    func_name = funcCall["funcname"][-1]["String"]["str"]
    args = funcCall["args"]
    field = None
    func_type = None
    for elem in args:
        if "ColumnRef" in elem.keys():
            field = elem["ColumnRef"]["fields"][0]["String"]["str"]
        elif "A_Const" in elem.keys():
            func_type = elem["A_Const"]["val"]["String"]["str"]
    if func_name == "date_part":
        return {"field": field, "func": {"pre": "datetime(", "post": ")." + func_type}}
    elif func_name == "avg":
        return {"field": field, "func": {"pre": "avg(", "post": ")"}}
    elif func_name == "count":
        return {"field": field, "func": {"pre": "count(", "post": ")"}}
    elif func_name == "sum":
        return {"field": field, "func": {"pre": "sum(", "post": ")"}}