## Row is already like a dictionary but because it is mutable and iterating over the rows changes this pointer
## this function solves the problem by creating a simple copy of the row.

def row_to_dictionary(row):
    dict_row = dict()
    attributes = row.table.colnames
    for key in attributes:
        dict_row[key] = row[key]
    return dict_row