from abstract_category.functor.functor_error import FunctorError


def construct_functor_to_graph_model(tables_to_nodes, tables_to_edges, source_fun, target_fun, rels_to_edges):
    target = {"objects": ["nodes", "edges"], "morphisms": [{"source": "edges", "morphism": "source",
                                                            "target": "nodes"}, {"source": "edges", "morphism": "target", "target": "nodes"}]}
    domain, fun = dict(), dict()
    domain["objects"], domain["morphisms"] = [], []

    if len(rels_to_edges) == len(tables_to_edges) == 0:
        for table in tables_to_nodes:
            domain["objects"].append(table["id"])
            fun[table["id"]] = "nodes"

    elif len(rels_to_edges) > 0 and len(tables_to_edges) == 0:

        for table in tables_to_nodes:
            domain["objects"].append(table["id"])
            fun[table["id"]] = "nodes"

        # Virtual edge table considered consisting of the foreign key and the primary key
        for rel in rels_to_edges:
            domain["objects"].append((rel["fk"], rel["pk"]))
            fun[(rel["fk"], rel["pk"])] = "edges"

        for rel in source_fun:
            domain["morphisms"].append(
                {"source": (rel["fk"], rel["pk"]), "morphism": rel["fk"], "target": rel["target"]})

            if rel["fk"] not in fun.keys():
                fun[rel["fk"]] = "source"
            else:
                raise FunctorError(
                    "The morphism " + rel["fk"] + " is already mapped to source function!")

        for rel in target_fun:
            domain["morphisms"].append(
                {"source": (rel["fk"], rel["pk"]), "morphism": rel["pk"], "target": rel["source"]})

            if rel["pk"] not in fun.keys():
                fun[rel["pk"]] = "target"
            else:
                raise FunctorError(
                    "The morphism " + rel["pk"] + " is already mapped to target function!")

    elif len(rels_to_edges) == 0 and len(tables_to_edges) > 0:

        for table in tables_to_nodes:
            domain["objects"].append(table["id"])
            fun[table["id"]] = "nodes"

        for table in tables_to_edges:
            domain["objects"].append(table["id"])
            fun[table["id"]] = "edges"

        for rel in source_fun:
            domain["morphisms"].append(
                {"source": rel["source"], "morphism": (rel["fk"], rel["pk"]), "target": rel["target"]})

            if (rel["fk"], rel["pk"]) not in fun.keys():
                fun[(rel["fk"], rel["pk"])] = "source"
            else:
                raise FunctorError(
                    "The morphism " + str((rel["fk"], rel["pk"])) + " is already mapped to source function!")

        for rel in target_fun:
            domain["morphisms"].append(
                {"source": rel["source"], "morphism": (rel["fk"], rel["pk"]), "target": rel["target"]})

            if (rel["fk"], rel["pk"]) not in fun.keys():
                fun[(rel["fk"], rel["pk"])] = "target"
            else:
                raise FunctorError(
                    "The morphism " + str((rel["fk"], rel["pk"])) + " is already mapped to target function!")
    else:
        raise FunctorError("""
                            The transformation, where relationships and tables are mapped to edges simultaneously, is not yet supported. 
    
                            The same result can be achieved by performing two transformations separately for relationships and tables.

                            """)

    return { "domain": domain, "functor": fun, "target": target }
