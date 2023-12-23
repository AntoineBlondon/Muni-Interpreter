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
            yield str(runtime.evaluate(stmt))
    else:
        yield str(runtime.evaluate(ast))

def run(code):
    ast = parser.parse(code)
    return run_program(ast)

def main():
    if len(sys.argv) != 2:
        print("Usage: python program.py <filename>")
        sys.exit(1)

    file_path = sys.argv[1]
    ast = parse_file(file_path)
    return run_program(ast)

if __name__ == "__main__":
    main()
