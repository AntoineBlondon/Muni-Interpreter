import sys
import os
from lexer import lexer
from runtime import run_ast
from mparser import parser

def read_file(filename):
    """Read a file and return its content."""
    try:
        with open(filename, 'r') as f:
            return f.read(), os.path.abspath(filename)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def lex_input(input_text):
    """Lex the input text and return tokens."""
    lexer.input(input_text)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))
    return tokens

def parse_input(input_text):
    """Parse the input text and return an AST."""
    parser.input_text = input_text  # Assuming this is necessary
    return parser.parse(input_text, lexer=lexer)  # Replace with your actual parser call


def main(filename, args):
    input_text, path = read_file(filename)
    if input_text is None:
        return
    
    tokens = lex_input(input_text)
    ast = parse_input(input_text)
    location = "/".join(path.split("/")[:-1])

    run_ast(ast, args=args, location=location)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <filename>")
    else:
        main(sys.argv[1], sys.argv[2:])