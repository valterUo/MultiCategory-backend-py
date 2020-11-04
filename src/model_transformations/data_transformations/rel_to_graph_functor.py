class RelToGraphFunctor:

    def __init__(self, tables_to_nodes, tables_to_edges, edge_source, edge_target):
        self.tables_to_nodes = tables_to_nodes
        self.tables_to_edges = tables_to_edges
        self.edge_source = edge_source
        self.edge_target = edge_target

    def get_tables_to_nodes(self):
        return self.tables_to_nodes

    def get_tables_to_edges(self):
        return self.tables_to_edges

    def get_edge_source(self):
        return self.edge_source

    def get_edge_target(self):
        return self.edge_target