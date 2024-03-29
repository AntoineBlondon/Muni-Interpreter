from muni_types import *
import codecs
import random
from muni_parser import parser
from muni_runtime import Runtime
from muni_ast_nodes import StatementList

def muni_print(value):
    print(codecs.decode(str(value), 'unicode_escape'))


def muni_type(value):
    try:
        return type(value).symbol()
    except:
        return type(value)

def muni_input(prompt):
    return Muni_String(input(codecs.decode(str(prompt), 'unicode_escape')))

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

def muni_split(value, sep=""):
    return Muni_List(str(value).split(str(sep))) if sep else Muni_List(str(value).split())

def muni_length(value):
    return Muni_Int(len(value))

def muni_shuffle(values):
    random.shuffle(list(values))
    return values

def muni_run_program(program, args=[]):
    program = str(program)
    args = [str(arg) for arg in list(args)]
    ast = parser.parse(program)
    runtime = Runtime()
    runtime.set_args(args)
    if isinstance(ast, StatementList):
        for stmt in ast.statements:
            runtime.evaluate(stmt)
    else:
        runtime.evaluate(ast)   