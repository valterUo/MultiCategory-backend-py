class Transformation:

    ## rel_schema_to_graph_functor is a mapping that takes a relational schema or part of the schema
    ## and maps it to edge -> node category that defines any graph

    def __init__(self, rel_db, graph_db, rel_to_graph_functor):
        self.rel_db = rel_db
        self.graph_db = graph_db
        self.rel_to_graph_functor = rel_to_graph_functor
        self.labels = []

    def get_rel_db(self):
        return self.rel_db
    
    def get_graph_db(self):
        return self.graph_db

    def get_rel_to_graph_functor(self):
        return self.rel_to_graph_functor

    def transform_table_into_collection_of_nodes(self, table_name):
        self.graph_db.create_index(self.rel_db, table_name, True)
        result = self.rel_db.query("SELECT * FROM " + table_name + ";")
        for result_dict in result:
            d = dict(result_dict)
            self.graph_db.create_and_return_node(table_name, d)

    def transform_tables_into_graph_db(self):
        tables = self.rel_to_graph_functor.get_tables_to_nodes()
        for table in tables:
            self.transform_table_into_collection_of_nodes(table)
        result = self.execute_read("MATCH (n) RETURN distinct labels(n)")
        for record in result:
            self.labels.append(record["labels(n)"])

    def collect_edge_data(self, rel1, rel2, relationship):
        res = "{ "
        for i, key in enumerate(relationship):
            if key != rel1 and key != rel2:
                if i == len(relationship):
                    res += key + " : " + relationship[key]
                else:
                    res += key + " : " + relationship[key] + ","
        res += res + "}"
        return res

    def create_edges_between_two_collections_of_nodes(self, label1, rel1, rel2, label2, edge_label1, edge_label2, relationship):
        edge_data = self.collect_edge_data(rel1, rel2, relationship)
        query = """
            MATCH (a: """ + label1 + """)
            MATCH (b: """ + label2 + """)
            WHERE a.""" + rel1 + """=""" + relationship[rel2] + """ 
            AND b.""" + rel2 + """=""" + relationship[rel2] + """
            CREATE (a) - [r : """ + edge_label1 + """_""" + edge_label2 + edge_data + """] -> (b)"""
        res = self.graph_db.execute_write(query)
        return res

    def query_relationships(self, table):
        query = "SELECT * FROM " + table + ";"
        result = self.rel_db.query(query)
        print(result)
        return result

    def create_edges(self):
        edges = self.rel_to_graph_functor.get_tables_to_edges()
        source_map = self.rel_to_graph_functor.get_edge_source()
        target_map = self.rel_to_graph_functor.get_edge_target()
        for edge in edges:
            table = edge["table"]
            edge_label1 = edge["source"]
            edge_label2 = edge["target"]
            rel1 = source_map[edge_label1][1]
            rel2 = target_map[edge_label2][1]
            relationships = self.query_relationships(table, edge_label1, edge_label2)
            label1 = source_map[edge_label1][0]
            label2 = target_map[edge_label2][0]
            for relationship in relationships:
                self.create_edges_between_two_collections_of_nodes(label1, rel1, rel2, label2, edge_label1, edge_label2, relationship)