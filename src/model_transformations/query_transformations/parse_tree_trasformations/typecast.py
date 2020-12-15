def pg_types_to_neo4j_types(type, value, type2 = "String"):
    if type == "timestamp":
        if type2 == "String":
            return "datetime('" + value + "')"
        elif type2 == "column":
            return "datetime(" + value + ")"