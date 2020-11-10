from dash_frontend.visualizations.nx_graph_visualization import general_nx_grah_to_cytoscape
import networkx as nx

def construct_postgres_schema(rel_db):
    res = rel_schema_to_nx_graph(rel_db)
    return general_nx_grah_to_cytoscape(res)

def rel_schema_to_nx_graph(rel_db):
    G = nx.DiGraph()
    schema = rel_db.get_schema()
    print(schema)
    nodes = []
    for key in schema:
        nodes.append((key, {"name": key, "attributes": ", ".join(schema[key])}))
    G.add_nodes_from(nodes)
    print(G)
    default_edges = rel_db.return_all_pk_fk_contrainsts()
    edges = []
    for e in default_edges:
        print(e, default_edges[e])
        for fk in default_edges[e]:
            if "target_table" in default_edges[e][fk].keys():
                edges.append((default_edges[e][fk]["target_table"], e, {"fk": fk, "pk": default_edges[e][fk]["primary_key_in_target_table"]}))
    G.add_edges_from(edges)
    return G

