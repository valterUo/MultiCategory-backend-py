import csv

def readCSV(filePath : str, delimiter : str, schema : [str], keyAttribute : str):
    table = []
    try:
        keyIndex = schema.index(keyAttribute)
        try:
            with open(filePath, newline='') as csvfile:
                            tableReader = csv.reader(csvfile, delimiter=delimiter)
                            next(tableReader)
                            for row in tableReader:
                                table.append((row[keyIndex], readRow(row, schema)))
        except:
           print("Error: Error while processing the cvs file!")
    except:
       print("Error: Key attribute not in the provided schema!")
    return table
    

def readRow(row, schema):
    newRow = []
    for i in range(len(schema)):
        try:
            newRow.append((schema[i], row[i]))
        except:
            try:
                newRow.append((schema[i], None))
            except:
                print("Error: Schema does not match to data in the file!")
    return dict(newRow)


def readToTable(filePath : str, delimiter : str, schema : [str], keyAttribute : str):
    return dict(readCSV(filePath, delimiter, schema, keyAttribute))


def readEdges(filePath : str, delimiter : str, schema : [str], keyAttribute : str):
    edgesWithKeys = readCSV(filePath, delimiter, schema, keyAttribute)
    edges = []
    for e in edgesWithKeys:
        edges.append(e[1])
    return edges


def readNodesAndEdges(filePathNodes : str, filePathEdges : str, delimiterNodes : str, delimiterEdges : str, schemaNodes : [str], schemaEdges : [str], 
keyAttributeNodes : str, keyAttributeEdges : str, fromKeyAttribute : str, toKeyAttribute : str):
    nodesWithKey = readToTable(filePathNodes, delimiterNodes, schemaNodes, keyAttributeNodes)
    edges = readEdges(filePathEdges, delimiterEdges, schemaEdges, keyAttributeEdges)
    edgeList = []
    for e in edges:
        edgeList.append((frozenset(nodesWithKey.get(e.get(fromKeyAttribute)).items()), 
                            frozenset(nodesWithKey.get(e.get(toKeyAttribute)).items()), frozenset(e.items())))
    return edgeList
