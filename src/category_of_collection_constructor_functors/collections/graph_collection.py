import shelve
import networkx as nx
import csv
import os
import pickle

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
        self.vertex_dict = dict()
        self.edge_list = list()
        if vertex_info != None and edge_info != None and target_folder_path != None:
            base = os.path.basename(edge_info[0]["file_path"])
            filename = os.path.splitext(base)[0]
            file_extension = os.path.splitext(edge_info[0]["file_path"])[1]

            self.target_file_path = self.target_folder_path + "//" + self.name + ".pyc"

            file_exists = os.path.isfile(self.target_file_path)

            if not file_exists:
                graph = self.parse_directed_graph()
                print("Created edges: " + str(graph.number_of_edges()))
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

    def parse_directed_graph(self):
        DG = nx.DiGraph()
        if self.vertex_info == []:
            self.read_edges_to_list()
            DG.add_edges_from(self.edge_list)
            return DG
        else:
            self.read_edges_to_list()
            self.read_vertex_csv_to_dict()
            DG.add_edges_from(self.edge_list)
            for key in self.vertex_dict:
                for subkey in self.vertex_dict[key]:
                    DG.nodes[key][subkey] = self.vertex_dict[key][subkey]
            return DG

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
                        #print("Unicode error. The row is be skipped: ", row)
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