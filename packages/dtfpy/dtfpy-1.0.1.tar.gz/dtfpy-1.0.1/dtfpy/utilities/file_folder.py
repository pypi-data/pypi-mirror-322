import os
import shutil


def make_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def folder_path_of_file(path):
    return os.path.dirname(os.path.realpath(path))


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def copy_file(source, destination):
    make_directory(folder_path_of_file(destination))
    remove_file(destination)
    shutil.copy(source, destination)


def check_equality(file1, file2):
    if not os.path.exists(file1) or not os.path.exists(file2):
        return False

    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        while True:
            byte1 = f1.read(1)
            byte2 = f2.read(1)
            if byte1 != byte2:
                return False
            if not byte1:
                return True
