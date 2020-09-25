import networkx as nx
import csv
import os
import pickle
from category_of_collection_constructor_functors.collections.tree_collection import TreeCollection
from category_of_collection_constructor_functors.collections.table_collection import TableCollection
from category_of_collection_constructor_functors.collections.converged_collection_connection import ConvergedCollectionConnection

class GraphCollection:

    """
    This class utilizes shelves which stores dictionary data on dics and uses persistent memory.
    Access of the dictionary should be as fast as in-memory version.

    vertex_info = [ { file_path, schema, key_attribute_index, delimiter } ]

    edge_info = [ { file_path, schema, source_attribute_index,
        target_attribute_index, delimiter } ]

    1. Create edges in format [(source_id, target_id, dict), ...]
    2. Loop over vertex values and assign values to sources and targets using source_ids and target_ids

    """

    def __init__(self, name, vertex_info = None, edge_info = None, target_folder_path = None):
        self.name = name
        self.vertex_info = vertex_info
        self.edge_info = edge_info
        self.target_folder_path = target_folder_path
        self.target_file_path = None
        self.vertex_dict = dict()
        self.edge_list = list()
        self.converged_collections = []

        if vertex_info != None and edge_info != None and target_folder_path != None:
            base = os.path.basename(edge_info[0]["file_path"])
            # filename = os.path.splitext(base)[0]
            # file_extension = os.path.splitext(edge_info[0]["file_path"])[1]

            self.target_file_path = self.target_folder_path + "//" + self.name + ".pyc"

            file_exists = os.path.isfile(self.target_file_path)

            if not file_exists:
                graph = self.parse_directed_graph()
                print("Created edges: " + str(graph.number_of_edges()))
                print("Created nodes: " + str(graph.number_of_nodes()))
                print("Writing the graph...")
                nx.write_gpickle(graph, self.target_file_path,
                                protocol=pickle.HIGHEST_PROTOCOL)

    def get_name(self):
        return self.name

    def get_model(self):
        return "graph"

    def get_vertex_info(self):
        return self.vertex_info

    def get_edge_info(self):
        return self.edge_info

    def get_target_folder_path(self):
        return self.target_folder_path

    def get_target_file_path(self):
        return self.target_file_path

    def set_target_file_path(self, new_path):
        self.target_file_path = new_path

    def get_iterable_collection_of_objects(self):
        graph = self.get_graph()
        return list(graph.nodes.data()) + list(graph.edges.data())

    def get_converged_collections(self):
        return self.converged_collections

    def parse_directed_graph(self):
        G = nx.DiGraph()
        if self.vertex_info == []:
            self.read_edges_to_list()
            G.add_edges_from(self.edge_list)
            return G
        else:
            self.read_edges_to_list()
            self.read_vertex_csv_to_dict()
            G.add_edges_from(self.edge_list)
            for key in self.vertex_dict:
                try:
                    for attribute in self.vertex_dict[key]:
                        try:
                            G.nodes[key][attribute] = self.vertex_dict[key][attribute]
                        except KeyError:
                            print("KeyError with key " + key + " at value " + str(self.vertex_dict[key]))
                            print("""This warning indicates that the vertex file contained more nodes than the edge file had connections. 
                            The vertex will be added as an isolated vertex with no edge connections.""")
                            G.add_nodes_from([(key, self.vertex_dict[key])])
                            break
                except KeyError:
                            print("KeyError with key " + key)
            return G

    def read_vertex_csv_to_dict(self):
        for vertex in self.vertex_info:
            file_path = vertex["file_path"]
            schema = vertex["schema"]
            key_attribute_index = vertex["key_attribute_index"]
            delimiter = vertex["delimiter"]
            with open(file_path, encoding='utf8') as csvfile:
                table_reader = csv.reader(csvfile, delimiter=delimiter)
                next(table_reader)  # Remove headers from csv file
                while True:
                    try:
                        row = next(table_reader)
                        self.vertex_dict[row[key_attribute_index]] = self.read_row(row, schema)
                    except StopIteration:
                        break
                    except csv.Error:
                        print("Error while processing the row: ", row)
                    except UnicodeDecodeError:
                        print("Unicode error. The row is be skipped: ", row)
                        continue
                    except IndexError:
                        print("Index error on the row: ", row)
                        continue

    def read_row(self, row, schema):
        new_row = dict()
        for i in range(len(schema)):
            try:
                new_row[schema[i]] = row[i]
            except:
                try:
                    new_row[schema[i]] = None
                except:
                    print("Error: Schema does not match to data in the file!")
        return new_row

    def read_edges_to_list(self):
        for edge in self.edge_info:
            file_path = edge["file_path"]
            schema = edge["schema"]
            source_attribute_index = edge["source_attribute_index"]
            target_attribute_index = edge["target_attribute_index"]
            delimiter = edge["delimiter"]
            with open(file_path, encoding='utf8') as csvfile:
                table_reader = csv.reader(csvfile, delimiter=delimiter)
                print(next(table_reader))  # Remove headers from csv file
                while True:
                    try:
                        row = next(table_reader)
                        source = row[source_attribute_index]
                        target = row[target_attribute_index]
                        #item_list = [source, target]
                        #row = [e for e in row if e not in item_list]
                        self.edge_list.append((source, target, self.read_row(row, schema)))
                    except StopIteration:
                        break
                    except csv.Error:
                        print("Error while processing the row: ", row)
                    except UnicodeDecodeError:
                        print("Unicode error. The row is be skipped: ", row)
                        continue
                    except IndexError:
                        print("Index error on the row: ", row)
                        continue

    def get_graph(self):
        return nx.read_gpickle(self.target_file_path)

    def append_to_collection(self, new_data_point):
        if self.target_file_path == None:
            self.target_file_path = self.target_folder_path + "//" + self.name + ".pyc"
        file_exists = os.path.isfile(self.target_file_path)

        if not file_exists:
            nx.write_gpickle(nx.DiGraph(), self.target_file_path, protocol=pickle.HIGHEST_PROTOCOL)

        G = nx.read_gpickle(self.target_file_path)

        if type(new_data_point) == tuple:
            if len(new_data_point) == 2:
                G.add_nodes_from([new_data_point])
            elif len(new_data_point) == 3:
                G.add_edges_from([new_data_point])
        elif type(new_data_point) == list:
            nodes, edges = [], []
            for data_point in new_data_point:
                if len(data_point) == 2:
                    nodes.append(data_point)
                elif len(data_point) == 3:
                    edges.append(data_point)
            G.add_nodes_from(nodes)
            G.add_edges_from(edges)
        nx.write_gpickle(G, self.target_file_path, protocol=pickle.HIGHEST_PROTOCOL)

    def get_length(self):
        if self.target_file_path != None:
            G = nx.read_gpickle(self.target_file_path)
            return G.number_of_nodes() + G.number_of_edges()
        else:
            return 0

    def add_converged_collection(self, name, model_category_connections_for_collection, target_folder_path):
        for connection in model_category_connections_for_collection:
            model = connection.get_target_model_category().get_model()
            target_collection = None
            if model == "relational":
                target_collection = TableCollection(name, h5file_path= target_folder_path + "\\" + name + ".h5")
            elif model == "graph":
                target_collection = GraphCollection(name, target_folder_path=target_folder_path)
            elif model == "tree":
                target_collection = TreeCollection(name, target_file_path=target_folder_path)
            target_collection.add_converged_collections(name + "_sub", connection.get_target_model_category().get_converged_model_categories(), target_folder_path)
            self.converged_collections.append(ConvergedCollectionConnection(self, connection.get_domain_id(), target_collection, connection.get_target_id()))
