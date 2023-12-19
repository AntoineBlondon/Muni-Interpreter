from ply import lex
from muni_types import *


# Dictionary of keywords
keywords = {
    'int': 'INT',       # For declaring integer variables
    'based': 'BASED',   # For declaring based number variables
    'complex': 'COMPLEX', # For declaring complex number variables
    'float': 'FLOAT',   # For declaring float variables
    'string': 'STRING', # For declaring string variables
    'boolean': 'BOOLEAN',     # For declaring boolean variables
    'void': 'VOID',       # For declaring void variables
    'list': 'LIST',     # For list data type
    'dict': 'DICT',     # For dictionary data type
    'for': 'FOR',       # For 'for' loops
    'while': 'WHILE',   # For 'while' loops
    'until': 'UNTIL',   # For 'until' loops
    'if': 'IF',         # For 'if' statements
    'else': 'ELSE',     # For 'else' statements
    'switch': 'SWITCH', # For 'switch' statements
    'case': 'CASE',     # For 'case' in switch statements
    'default': 'DEFAULT', # For 'default' in switch statements
    'break': 'BREAK',   # For breaking out of loops or switch statements
    #'try': 'TRY',       # For 'try' in exception handling
    #'catch': 'CATCH',   # For 'catch' in exception handling
    'import': 'IMPORT', # For importing modules
    'as': 'AS',         # For aliasing in imports
    'return': 'RETURN',  # For returning values from functions
    'in': 'IN', 
    'signal': 'SIGNAL',
    'emit': 'EMIT',
    'watch': 'WATCH',
    'when': 'WHEN',

}

tokens = [
    
    'IDENTIFIER',
    
    'EQUALS', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COLON', 'PLUSEQ', 'MINUSEQ', 'MULEQ', 'DIVEQ', 'MODEQ',
    'MODULUS',
    #'LARROW', 
    'RARROW',
    'UNTYPED', 'LBRACKET', 'RBRACKET', 'AT',
    

    'SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'PIPE',
    'EXCLAMATION', 'AMPERSAND', 'HAT',
    'NUMBER', 'IMAGINARY_NUMBER', 'BASED_NUMBER', 'STRING_LITERAL', 'IMPORT_LITERAL',
] + list(keywords.values())



# Operator tokens
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MUL = r'\*'
t_DIV = r'/'
t_PLUSEQ = r'\+='
t_MINUSEQ = r'-='
t_MULEQ = r'\*='
t_DIVEQ = r'/='
t_MODULUS = r'%'
t_MODEQ = r'%='

# Delimiter tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'

#t_LARROW = r'<-'
t_RARROW = r'->'


# Additional delimiter tokens
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMI = r';'
t_COMMA = r','
t_COLON = r':'
t_PIPE = r'\|'


t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='

t_EXCLAMATION = r'!'
t_AMPERSAND = r'&'
t_HAT = r'\^'

t_UNTYPED = r'\?'
t_AT = r'@'


# Boolean values
def t_BOOLEAN(t):
    r'true|false'
    t.value = Muni_Boolean(t.value == 'true')
    return t

def t_BASED_NUMBER(t):
    r'-?\d+@[\da-zA-Z]+'
    base, value = t.value.split('@')
    t.value = Muni_BasedNumber(value, int(base))
    return t

def t_IMAGINARY_NUMBER(t):
    r'-?\d+(\.\d+)?[jJ]|-?[jJ]'
    # Extract the numerical part and create an imaginary number representation
    if len(t.value) == 1:
        t.value = Muni_Complex(0,1)
        return t
    if len(t.value) == 2 and t.value.startswith('-'):  # For cases like "-j"
        t.value = Muni_Complex(0, -1)
        return t
    num_part = t.value[:-1]  # Remove the 'j'
    t.value = Muni_Complex(0,float(num_part))  # Assuming Muni_Imaginary is a class to handle imaginary numbers
    return t

# Literals
def t_NUMBER(t):
    r'-?\d+(\.\d+)?([eE][-+]?\d+)?'
    if '.' in t.value or 'e' in t.value or 'E' in t.value:
        t.value = Muni_Float(float(t.value))
    else:
        t.value = Muni_Int(int(t.value))
    return t





def t_STRING_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove the quotes
    t.value = Muni_String(t.value)
    return t

def t_IMPORT_LITERAL(t):
    r'<[a-zA-Z0-9_.:]+>'
    t.value = t.value[1:-1]  # Remove the < and >
    return t

# Identifier and keyword matching
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'IDENTIFIER')
    return t



# Comments
def t_comment_singleline(t):
    r'\#.*'
    pass  # No return value. Token discarded

def t_comment_multiline(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')  # Update the line numbers
    pass  # No return value. Token discarded


t_ignore = ' \t'

# Newlines
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Errors
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, column {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()
