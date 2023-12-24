import sys
from muni_types import *
from muni_parser import *
from muni_runtime import Runtime
from muni_ast_nodes import *
import argparse
import sys
from muni_lexer import lexer


def run_program(ast):
    runtime = Runtime()
    if isinstance(ast, StatementList):
        for stmt in ast.statements:
            runtime.evaluate(stmt)
    else:
        runtime.evaluate(ast)

def run_program_with_results(ast):
    runtime = Runtime()
    if isinstance(ast, StatementList):
        for stmt in ast.statements:
            yield str(runtime.evaluate(stmt))
    else:
        yield str(runtime.evaluate(ast))

def run(code):
    ast = parser.parse(code)
    return run_program_with_results(ast) 

def main():
    argparser = argparse.ArgumentParser(description='Muni Programming Language Interpreter')
    argparser.add_argument('file', help='the Muni source file to interpret')
    argparser.add_argument('-l', '--lexer', action='store_true', help='print the lexer output')
    argparser.add_argument('-p', '--parser', action='store_true', help='print the parser output')

    args = argparser.parse_args()

    with open(args.file, 'r') as file:
        content = file.read()

    if args.lexer:
        lexer.input(content)
        for token in lexer:
            print(token)

    if args.parser:
        ast = parser.parse(content)
        print(ast)

    if not args.lexer and not args.parser:
        ast = parser.parse(content)
        run_program(ast)  

if __name__ == "__main__":
    main()