import os
from tables import *
import csv
from category_of_collection_constructor_functors.collections.collection_errors import UnknownRelationalFileExtension, DatabaseFileDoesNotExists


class TableCollection:

    """
    This class utilizes pytables which stores relational data in h5files and uses persistent memory. 
    PyTables requires some parameter modifications to chunk sizes because the output file size is huge.
    JSON file is assumed to be "flat" i.e. there are no JSON objects inside JSON objects.

    Different data types that are supported:

            StringCol(16)   # 16-character String
            Int64Col()      # Signed 64-bit integer
            UInt16Col()     # Unsigned short integer
            UInt8Col()      # unsigned byte
            Int32Col()      # 32-bit integer
            Float32Col()    # float  (single-precision)
            Float64Col()    # double (double-precision)
            
    """

    def __init__(self, name, attributes_datatypes_dict=None, source_file_path=None, h5file_path=None, delimiter="|", primary_key=None):
        self.name = name
        self.attributes_datatypes_dict = attributes_datatypes_dict
        self.source_file_path = source_file_path
        self.h5file_path = h5file_path
        self.h5file = None
        self.table = None
        self.primary_key = primary_key
        self.converged_collections = []
        if attributes_datatypes_dict != None and source_file_path != None and h5file_path != None:
            base = os.path.basename(source_file_path)
            filename = os.path.splitext(base)[0]
            file_extension = os.path.splitext(source_file_path)[1]
            self.h5file_path = h5file_path + "//" + filename + ".h5"
            h5file_exists = os.path.isfile(self.h5file_path)
            if not h5file_exists:
                print("The database file in path " + self.h5file_path +
                      " does not exists. The file will be created.")
                self.create_h5_file(file_extension, delimiter)
            else:
                print("The database file for " + self.name + " exsists.")
            self.h5file = open_file(
                self.h5file_path, mode="r+", title=self.name + " file")
            self.table = self.h5file.get_node("/" + self.name, self.name)
            if self.primary_key != None:
                if not self.table.cols._f_col(primary_key).is_indexed:
                    print("Creating index for column: " + primary_key)
                    self.table.cols._f_col(primary_key).create_index()
                else:
                    print("Index has already been created for " + primary_key)

    def get_name(self):
        return self.name

    def get_model(self):
        return "relational"

    def get_source_file_path(self):
        return self.source_file_path

    def get_attributes_datatypes_dict(self):
        return self.attributes_datatypes_dict

    def get_target_file_path(self):
        return self.h5file_path

    def get_iterable_collection_of_objects(self):
        if self.table == None:
            self.h5file = open_file(
                self.h5file_path, mode="r+", title=self.name + " file")
            self.table = self.h5file.get_node("/" + self.name, self.name)
        return self.table

    def get_rows(self):
        if self.table != None:
            return self.table.iterrows()
        else:
            raise DatabaseFileDoesNotExists(
                "h5file is not defined", "h5file is not defined")

    def get_table(self):
        return self.table

    def set_h5file_path(self, new_h5file_path):
        self.h5file_path = new_h5file_path

    def set_attributes_datatypes_dict(self, new_attributes_datatypes_dict):
        self.attributes_datatypes_dict = new_attributes_datatypes_dict

    def add_converged_collection(self, new):
        self.converged_collections.append(new)

    def create_h5_file(self, file_extension, delimiter):
        self.h5file = open_file(
            self.h5file_path, mode="w", title=self.name + " file")
        self.group = self.h5file.create_group(
            "/", self.name, self.name + " information")
        self.table = self.h5file.create_table(
            self.group, self.name, self.attributes_datatypes_dict, self.name + " table")
        if file_extension == ".csv" or file_extension == ".table" or file_extension == ".txt":
            self.import_csv_to_table(delimiter)
        elif file_extension == ".json":
            self.import_json_to_table(delimiter)
        else:
            raise UnknownRelationalFileExtension(
                "The file extension is not supported. Currently only csv, table, txt and json are supported.", file_extension)
        self.h5file.close()

    def import_csv_to_table(self, delimiter):
        with open(self.source_file_path, encoding='utf8') as csvfile:
            table_reader = csv.reader(csvfile, delimiter=delimiter)
            # remove the first line containing the attributes
            print("The header will be ignored: " +
                  ",".join(next(table_reader)))
            key_list = list(self.attributes_datatypes_dict.keys())
            tablerow = self.table.row
            while True:
                try:
                    row = next(table_reader)
                    for j in range(len(key_list)):
                        try:
                            tablerow[key_list[j]] = row[j]
                        except TypeError:
                            #print(key_list[j], row[j], "with type " + str(type(row[j])))
                            tablerow[key_list[j]] = row[j].encode("utf-8")
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

    def append_to_collection(self, new_data_point):
        h5file_exists = os.path.isfile(self.h5file_path)
        h5file, table = None, None
        if not h5file_exists:
            print(self.h5file_path)
            h5file = open_file(self.h5file_path, mode="w",
                               title=self.name + " file")
            group = h5file.create_group(
                "/", self.name, self.name + " information")
            table = h5file.create_table(
                group, self.name, self.attributes_datatypes_dict, self.name + " table")
        else:
            h5file = open_file(self.h5file_path, mode="r+",
                               title=self.name + " file")
            table = h5file.get_node("/" + self.name, self.name)
        tablerow = table.row
        if type(new_data_point) == dict:
            self.add_to_tablerow(tablerow, new_data_point)
        elif type(new_data_point) == list:
            for elem in new_data_point:
                self.add_to_tablerow(tablerow, elem)
        table.flush()
        h5file.close()

    def add_to_tablerow(self, tablerow, new_data_point):
        for elem in new_data_point:
            for attribute in elem:
                try:
                    tablerow[attribute] = elem[attribute]
                except TypeError:
                    tablerow[attribute] = elem[attribute].encode("utf-8")
            tablerow.append()

    def get_length(self):
        if self.h5file_path == None:
            return 0
        table = self.get_iterable_collection_of_objects()
        return table.nrows
