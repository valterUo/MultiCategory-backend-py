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

    """

    def __init__(self, name, vertex_info, edge_info, target_folder_path):
        self.name = name
        self.vertex_info = vertex_info
        self.edge_info = edge_info
        self.target_folder_path = target_folder_path
        self.vertex_dict = dict()
        self.edge_list = list()

        base = os.path.basename(edge_info[0]["file_path"])
        filename = os.path.splitext(base)[0]
        file_extension = os.path.splitext(edge_info[0]["file_path"])[1]

        self.target_file_path = self.target_folder_path + "//" + self.name + ".pyc"

        file_exists = os.path.isfile(self.target_file_path)

        if not file_exists:
            graph = self.parse_directed_graph()
            nx.write_gpickle(graph, self.target_file_path,
                             protocol=pickle.HIGHEST_PROTOCOL)

    def get_name(self):
        return self.name

    def get_vertex_info(self):
        return self.vertex_info

    def get_edge_info(self):
        return self.edge_info

    def get_target_folder_path(self):
        return self.target_folder_path

    def get_target_file_path(self):
        return self.target_file_path

    def get_iterable_collection_of_objects(self):
        graph = self.get_graph()
        return list(graph.nodes) + list(graph.edges)

    def parse_directed_graph(self):
        DG = nx.DiGraph()
        if self.vertex_info == []:
            self.read_edges_to_list_without_vertex_info()
            for edge in self.edge_list:
                DG.add_edge(edge[0], edge[1], object=edge[2])
            return DG
        else:
            self.read_edges_to_list_without_vertex_info()
            self.read_vertex_csv_to_dict()
            for edge in self.edge_list:
                DG.add_edge(
                    frozenset(self.vertex_dict[edge[0]].items()), frozenset(self.vertex_dict[edge[1]].items()), object=edge[2])
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
                        self.vertex_dict[row[key_attribute_index]] = self.read_row(
                            row, schema)
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

    def read_edges_to_list_without_vertex_info(self):
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
                        item_list = [source, target]
                        row = [e for e in row if e not in item_list]
                        self.edge_list.append([source, target, frozenset(self.read_row(row, schema).items())])
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