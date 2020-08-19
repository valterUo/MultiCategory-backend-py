import os

def parse_file_path(old_path, new_file_name):
        dir_name = os.path.dirname(old_path)
        # base = os.path.basename(old_path)
        # filename = os.path.splitext(base)[0]
        file_extension = os.path.splitext(old_path)[1]
        return dir_name + "\\" + new_file_name + file_extension

def parse_file_name(path):
    base = os.path.basename(path)
    filename = os.path.splitext(base)[0]
    return filename