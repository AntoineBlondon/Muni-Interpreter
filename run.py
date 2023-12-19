import sys
from muni_types import *
from muni_parser import *
from muni_runtime import Runtime
from muni_ast_nodes import *

 # Returns an AST

def run_program(ast):
    runtime = Runtime()
    if isinstance(ast, StatementList):
        for stmt in ast.statements:
            runtime.evaluate(stmt)
    else:
        runtime.evaluate(ast)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    ast = parse_file(file_path)
    run_program(ast)

if __name__ == "__main__":
    main()
