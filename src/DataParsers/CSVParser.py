import csv

def readToTable(filePath : str, delimiter : str, schema : [str], keyAttribute : str):
    table = []
    try:
        keyIndex = schema.index(keyAttribute)
        try:
            with open(filePath, newline='') as csvfile:
                            tableReader = csv.reader(csvfile, delimiter=delimiter)
                            next(tableReader)
                            for row in tableReader:
                                table.append((row[keyIndex], processRow(row, schema)))
        except:
           print("Error: Error while processing the cvs file!")
    except:
       print("Error: Key attribute not in the provided schema!")
    return dict(table)
    

def processRow(row, schema):
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