import os
from tables import *
import csv
import json
from json import JSONDecodeError
from category_of_collection_constructor_functors.collections.collection_errors import UnknownRelationalFileExtension

class TableCollection:

    """
    This class utilizes pytables which stores relational data in h5files and uses persistent memory. 
    PyTables requires some parameter modifications to chunk sizes because the output file size is huge.
    JSON file is assumed to be "flat" i.e. there are no JSON objects inside JSON objects.
    """

    def __init__(self, name, attributes_datatypes_dict, source_file_path, h5file_path, delimiter = "|"):
        self.name = name
        self.source_file_path = source_file_path
        self.attributes_datatypes_dict = attributes_datatypes_dict
        #dir_name = os.path.dirname(source_file_path)
        base = os.path.basename(source_file_path)
        filename = os.path.splitext(base)[0]
        file_extension = os.path.splitext(source_file_path)[1]
        self.h5file_path = h5file_path + "//" + filename + ".h5"
        h5file_exists = os.path.isfile(self.h5file_path)
        if not h5file_exists:
            self.create_h5_file(file_extension, delimiter)

    def get_rows(self):
        self.h5file = open_file(self.h5file_path, mode="r", title= self.name + " file")
        table = self.h5file.get_node("/" + self.name, self.name)
        return table.iterrows()


    def create_h5_file(self, file_extension, delimiter):
        self.h5file = open_file(self.h5file_path, mode="w", title= self.name + " file")
        self.group = self.h5file.create_group("/", self.name, self.name + " information")
        self.table = self.h5file.create_table(self.group, self.name, self.attributes_datatypes_dict, self.name + " table")
        if file_extension == ".csv" or file_extension == ".table" or file_extension == ".txt":
            self.import_csv_to_table(delimiter)
        elif file_extension == ".json":
            self.import_json_to_table(delimiter)
        else:
            raise UnknownRelationalFileExtension("The file extension is not supported. Currently only csv, table, txt and json are supported.", file_extension)
        self.h5file.close()


    def import_csv_to_table(self, delimiter):
        i = 0
        with open(self.source_file_path, encoding='utf8') as csvfile:
            table_reader = csv.reader(csvfile, delimiter=delimiter)
            print("The header will be ignored: " + ",".join(next(table_reader))) #remove the first line containing the attributes
            key_list = list(self.attributes_datatypes_dict.keys())
            tablerow = self.table.row
            while True:
                try:
                    row = next(table_reader)
                    for j in range(len(key_list)):
                        tablerow[key_list[j]] = row[j]
                    tablerow.append()
                except StopIteration:
                    print("Flushing...")
                    self.table.flush()
                    break
                except csv.Error:
                    print("Error while processing the row: ", row)
                except UnicodeDecodeError:
                    #print("Unicode error. The row is be skipped: ", row)
                    continue
                except IndexError:
                    print("Index error on the row: ", row)
                    continue


    def import_json_to_table(self, delimiter):
        try:
            data_set = json.load(json_file)
        except JSONDecodeError:
            print("JSON Decoder Error. Trying read line by line.")
            try:
                data_set = []
                json_file.seek(0,0)  
                for json_line in json_file.readlines():
                    parsed_line = json.loads(json_line)
                    data_set.append(parsed_line)
            except Exception as e:
                print("JSON file is invalid: ", e)
        return data_set