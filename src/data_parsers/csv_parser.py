import csv
import networkx as nx
import pickle

def read_to_table(filePath: str, delimiter: str, schema: [str], keyAttribute):
    table = dict()
    try:
        if type(keyAttribute) == list:
            key_indexes = []
            for attribute in keyAttribute:
                key_indexes.append(schema.index(attribute))
        else:
            key_indexes = [schema.index(keyAttribute)]
        try:
            with open(filePath) as csvfile:
                            tableReader = csv.reader(
                                csvfile, delimiter=delimiter)
                            next(tableReader)
                            for row in tableReader:
                                key = ""
                                for key_index in key_indexes:
                                    key = key + row[key_index]
                                table[key] = read_row(row, schema)
        except:
           print("Error: Error while processing the csv file!")
    except:
       print("Error: Key attribute not in the provided schema!")
    return table


def read_row(row, schema):
    newRow = dict()
    for i in range(len(schema)):
        try:
            newRow[schema[i]] = row[i]
        except:
            try:
                newRow[schema[i]] = None
            except:
                print("Error: Schema does not match to data in the file!")
    return newRow


def read_nodes_and_edges(file_dictionaries):
    DG = nx.DiGraph()
    nodeDict, edgeDict = file_dictionaries["vertex"], file_dictionaries["edge"]
    nodes_with_key, edges = dict(), dict()
    if file_dictionaries["vertex"][0]["filePath"] == file_dictionaries["edge"][0]["filePath"]:
        for edge in edgeDict:
            edges.update(read_to_table(edge["filePath"], edge["separator"], edge["schema"], edge["keyAttribute"]))
        for edge in edgeDict:
            for e in edges.values():
                DG.add_edge(e.get(edge["fromKeyAttribute"]), e.get(edge["toKeyAttribute"]), object=frozenset(e.items()))
    else:
        for node in nodeDict:
            nodes_with_key.update(read_to_table(node["filePath"], node["separator"], node["schema"], node["keyAttribute"]))
        for edge in edgeDict:
            edges.update(read_to_table(edge["filePath"], edge["separator"], edge["schema"], edge["keyAttribute"]))
            for e in edges.values():
                DG.add_edge(frozenset(nodes_with_key.get(e.get(edge["fromKeyAttribute"])).items()),
                                frozenset(nodes_with_key.get(e.get(edge["toKeyAttribute"])).items()), 
                                object=frozenset(e.items()))
    return DG

def dump_big_file_into_pickle(data_set, file_name):
    with open(file_name, "wb+") as db_file:
        pickle.dump(data_set, db_file, protocol=pickle.HIGHEST_PROTOCOL)
    return file_name
