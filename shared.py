import os

OUTPUT = './output/'


def output_dir(name):
    path = OUTPUT + name
    if not os.path.exists(path):
        os.makedirs(path)
    return path
