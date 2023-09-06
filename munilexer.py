from ply import lex
    


# Dictionary of keywords
keywords = {
    'int': 'INT',       # For declaring integer variables
    'float': 'FLOAT',   # For declaring float variables
    'string': 'STR', # For declaring string variables
    'boolean': 'BOOL',     # For declaring boolean variables
    'void': 'VOID',       # For declaring void variables
    'list': 'LIST',     # For list data type
    #'dict': 'DICT',     # For dictionary data type
    'for': 'FOR',       # For 'for' loops
    'while': 'WHILE',   # For 'while' loops
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
    'true': 'TRUE',     # For declaring boolean variables
    'false': 'FALSE',   # For declaring boolean variables 
    'in': 'IN', 
}

tokens = [
    
    'IDENTIFIER',
    
    'EQUALS', 'PLUS', 'MINUS', 'MUL', 'DIV', 'GT', 'LT', 'GE', 'LE', 'EQ', 'NE', 'COLON', 'PLUSEQ', 'MINUSEQ', 'MULEQ', 'DIVEQ',
    'LARROW', 'RARROW',
    'UNTYPED', 'LBRACKET', 'RBRACKET', 'AT',
    #'TERNARY_QUESTION', 'TERNARY_COLON',
    
    'SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'PIPE',
    
    'INTEGER_LITERAL', 'STRING_LITERAL', 'FLOAT_LITERAL',
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


# Delimiter tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LARROW = r'<-'
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

t_UNTYPED = r'\?'
t_AT = r'@'


# Boolean values
def t_TRUE(t):
    r'true'
    t.type = 'TRUE'  # Set the type to 'TRUE'
    t.value = True   # Set the value to Python's True
    return t

def t_FALSE(t):
    r'false'
    t.type = 'FALSE'  # Set the type to 'FALSE'
    t.value = False   # Set the value to Python's False
    return t

# Literals
def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
def t_INTEGER_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t



def t_STRING_LITERAL(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove the quotes
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

