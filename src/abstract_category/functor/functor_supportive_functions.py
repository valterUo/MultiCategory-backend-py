from abstract_category.functor.functor_error import FunctorError

def construct_functor_to_graph_model(tables_to_nodes, tables_to_edges, source_fun, target_fun):

    target = {"objects": ["nodes", "edges"], "morphisms": [{"source": "edges", "morphism": "source",
        "target": "nodes"}, {"source": "edges", "morphism": "target", "target": "nodes"}]}
    domain, fun = dict(), dict()
    domain["objects"], domain["morphisms"] = [], []
    
    for table in tables_to_nodes:
        domain["objects"].append(table["id"])
        fun[table["id"]] = "nodes"

    for table in tables_to_edges:
        domain["objects"].append(table["id"])
        fun[table["id"]] = "edges"

    for rel in source_fun:
        domain["morphisms"].append(
            {"source": rel["target"], "morphism": (rel["fk"], rel["pk"]), "target": rel["source"]})
        
        if (rel["fk"], rel["pk"]) not in fun.keys():
            fun[(rel["fk"], rel["pk"])] = "source"
        else:
            raise FunctorError("The morphism " + str((rel["fk"], rel["pk"])) + " is already mapped to source function!")
    
    for rel in target_fun:
        domain["morphisms"].append(
            {"source": rel["target"], "morphism": (rel["fk"], rel["pk"]), "target": rel["source"]})
        
        if (rel["fk"], rel["pk"]) not in fun.keys():
            fun[(rel["fk"], rel["pk"])] = "target"
        else:
            raise FunctorError("The morphism " + str((rel["fk"], rel["pk"])) + " is already mapped to target function!")
    
    return domain, fun, target