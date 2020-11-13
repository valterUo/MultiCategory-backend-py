from model_transformations.data_transformations.data_transformation_error import DataTransformationError


class Transformation:

    ## rel_schema_to_graph_functor is a mapping that takes a relational schema or part of the schema
    ## and maps it to edge -> node category that defines any graph

    def __init__(self, rel_db, graph_db, rel_to_graph_functor=[]):
        self.rel_db = rel_db
        self.graph_db = graph_db
        self.rel_to_graph_functor = rel_to_graph_functor
        self.labels = []
        self.transform()

    def get_rel_db(self):
        return self.rel_db

    def get_graph_db(self):
        return self.graph_db

    def get_rel_to_graph_functor(self):
        return self.rel_to_graph_functor

    def transform(self):
        if len(self.rel_to_graph_functor.get_tables_to_nodes()) == 0:
            self.graph_db.transform_tables_into_graph_db(self.rel_db)
            self.graph_db.create_edges(self.rel_db)
        else:
            self.transform_tables_into_graph_db()
            self.create_edges()

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
        result = self.graph_db.execute_read(
            "MATCH (n) RETURN distinct labels(n)")
        for record in result:
            self.labels.append(record["labels(n)"])

    def collect_edge_data(self, rel1, rel2, relationship):
        res = "{ "
        for key in relationship:
            if key != rel1 and key != rel2:
                res += str(key) + " : '" + str(relationship[key]) + "', "
        res = res[:-2] + " }"
        return res

    def create_edges_between_two_collections_of_nodes(self, label1, rel1, rel2, label2, edge_label1, edge_label2, relationship):
        edge_data = self.collect_edge_data(
            edge_label1, edge_label2, relationship)
        query = """
            MATCH (a: """ + label1 + """)
            MATCH (b: """ + label2 + """)
            WHERE a.""" + rel1 + """=""" + str(relationship[edge_label1]) + """ 
            AND b.""" + rel2 + """=""" + str(relationship[edge_label2]) + """
            CREATE (a) - [r : """ + edge_label1 + """_""" + edge_label2 + edge_data + """] -> (b)"""
        #res = self.graph_db.execute_write(query)
        return res

    def query_relationships(self, table):
        query = "SELECT * FROM " + table + ";"
        result = self.rel_db.query(query, "dict")
        return result

    def create_edges(self):
        edges = self.rel_to_graph_functor.get_tables_to_edges()
        source_map = self.rel_to_graph_functor.get_edge_source()
        target_map = self.rel_to_graph_functor.get_edge_target()
        domain_morphisms = self.rel_to_graph_functor.get_morphisms_of_domain_category()
        for fk_table in edges:
            fk_source, fk_target, pk_source, pk_target = None, None, None, None
            pk_table_source, pk_table_target = None, None
            for key in source_map:
                if len(key) != 2:
                    raise DataTransformationError(
                        "Source map is in wrong format ", key)
                fk_source = key[0]
                pk_source = key[1]
            for key in target_map:
                if len(key) != 2:
                    raise DataTransformationError(
                        "Target map is in wrong format ", key)
                fk_target = key[0]
                pk_target = key[1]
            relationships = self.query_relationships(fk_table)
            if fk_source is not None and pk_source is not None:
                for mor in domain_morphisms:
                    print(mor)
                    if (fk_source, pk_source) in mor.values():
                        pk_table_source = mor["target"]
            if fk_target is not None and pk_target is not None:
                for mor in domain_morphisms:
                    if (fk_target, pk_target) in mor.values():
                        pk_table_target = mor["target"]
            if None in [fk_source, fk_target, pk_source, pk_target, pk_table_source, pk_table_target]:
                raise DataTransformationError("Some of the variables are not defined ", [
                                              fk_source, fk_target, pk_source, pk_target, pk_table_source, pk_table_target])
            print()
            print("fk_table: ", fk_table)
            print("fk_source: ", fk_source)
            print("fk_target: ", fk_target)
            print("pk_source: ", pk_source)
            print("pk_target: ", pk_target)
            print("pk_table_source: ", pk_table_source)
            print("pk_table_target: ", pk_table_target)
            print()
            for relationship in relationships:
                self.create_edges_between_two_collections_of_nodes(
                    pk_table_source, pk_source, pk_target, pk_table_target, fk_source, fk_target, relationship)
