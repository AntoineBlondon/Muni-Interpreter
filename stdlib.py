from muni_types import *

def muni_print(value):
    print(value)


def muni_type(value):
    return type(value).symbol()


def muni_input(prompt):
    return Muni_String(input(prompt))

def muni_read(filename):
    with open(str(filename), 'r') as f:
        return Muni_String(f.read())

def muni_write(filename, content):
    with open(str(filename), 'w') as f:
        f.write(str(content))

def muni_sort(values):
    return sorted(values)