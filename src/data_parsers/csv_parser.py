import csv

def read_to_table(filePath: str, delimiter: str, schema: [str], keyAttribute):
    table = dict()
    try:
        if type(keyAttribute) == list:
            keyIndex = []
            for attribute in keyAttribute:
                keyIndex.append(schema.index(keyAttribute))
        else:
            keyIndex = [schema.index(keyAttribute)]
        try:
            with open(filePath) as csvfile:
                            tableReader = csv.reader(
                                csvfile, delimiter=delimiter)
                            next(tableReader)
                            for row in tableReader:
                                key = ""
                                for key_attribute in keyIndex:
                                    key = key + row[keyIndex]
                                table[row[key]] = readRow(row, schema)
        except:
           print("Error: Error while processing the cvs file!")
    except:
       print("Error: Key attribute not in the provided schema!")
    return table


def readRow(row, schema):
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


def readEdges(filePath: str, delimiter: str, schema: [str], keyAttribute: str):
    edges_with_keys = read_to_table(filePath, delimiter, schema, keyAttribute)
    edges = []
    for e in edges_with_keys:
        edges.append(e[1])
    return edges


def readNodesAndEdges(file_dictionaries):
    nodesWithKey = dict()
    edges, edgeList = [], []
    nodeDict, edgeDict = file_dictionaries["vertex"], file_dictionaries["edge"]
    for node in nodeDict:
        nodesWithKey.update(read_to_table(
            node["filePath"], ";", node["schema"], node["keyAttribute"]))
    for edge in edgeDict:
        edges = readEdges(edge["filePath"], ";",
                          edge["schema"], edge["keyAttribute"])
        for e in edges:
            edgeList.append((frozenset(nodesWithKey.get(e.get(edge["fromKeyAttribute"])).items()),
                             frozenset(nodesWithKey.get(e.get(edge["toKeyAttribute"])).items()), 
                             frozenset(e.items())))
    return edgeList

def dump_big_file_into_pickle(file_dictionaries, file_name):
    with open(file_name) as db_file:
        pickle.dump(table, db_file, protocol=pickle.HIGHEST_PROTOCOL)
    return file_name
