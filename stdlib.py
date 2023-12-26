from muni_types import *
import random

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

def muni_join(values, sep):
    return str(sep).join(str(v) for v in values)

def muni_split(value, sep):
    return str(value).split(str(sep))

def muni_length(value):
    return len(value)

def muni_shuffle(values):
    random.shuffle(values)
    return values