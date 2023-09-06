from ply import yacc
from munilexer import tokens, keywords  # Import tokens from lexer.py

input_text = ""  # Global variable to hold the input text

def find_column(lexpos):
    global input_text
    last_cr = input_text.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = 0
    column = lexpos - last_cr
    return column


def p_program(p):
    'program : statements'
    p[0] = p[1]


def p_statements(p):
    '''statements : statement SEMI statements
                  | statement SEMI
                  | statement statements
                  | statement'''
    if p[1][0] in ['if', 'if-else', 'for_loop', 'while_loop', 'do_while_loop', 'function_declaration']:  # Add other statement types that don't require a semicolon
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]
    else:
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        elif len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]]
def p_function_declaration(p):
    '''function_declaration : type_specifier IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE EQUALS expression
                            | type_specifier IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE'''
    if len(p) == 11:
        p[0] = ('function_declaration', p[1], p[2], p[4], p[7], p[10], p.lineno(1), find_column(p.lexpos(1)))
    else:
        p[0] = ('function_declaration', p[1], p[2], p[4], p[7], None, p.lineno(1), find_column(p.lexpos(1)))




def p_parameters(p):
    '''parameters : type_specifier IDENTIFIER COMMA parameters
                  | type_specifier IDENTIFIER
                  | '''
    if len(p) == 5:
        p[0] = [(p[1], p[2])] + p[4]
    elif len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = []


def p_expression_function_call(p):
    '''expression  : IDENTIFIER LPAREN arguments RPAREN
                   | IDENTIFIER PIPE IDENTIFIER LPAREN arguments RPAREN'''
    if len(p) == 5:
        p[0] = ('function_call', p[1], p[3], p.lineno(1), find_column(p.lexpos(1)))
    else:
        namespaced_function = f"{p[1]}|{p[3]}"
        p[0] = ('function_call', namespaced_function, p[5], p.lineno(1), find_column(p.lexpos(1)))

def p_arguments(p):
    '''arguments : expression COMMA arguments
                 | expression
                 | '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []

def p_return_statement(p):
    'return_statement : RETURN expression SEMI'
    p[0] = ('return', p[2], p.lineno(1), find_column(p.lexpos(1)))

# Update statement rule
def p_statement(p):
    '''statement : declaration
                 | assignment
                 | function_declaration
                 | expression
                 | list_operation
                 | return_statement'''
    p[0] = p[1]


def p_import_statement(p):
    '''statement : IMPORT expression AS IDENTIFIER
                 | IMPORT expression'''
    if len(p) == 3:
        p[0] = ('import', p[2], p.lineno(1), find_column(p.lexpos(1)))
    else:
        p[0] = ('import', p[2], p[4], p.lineno(1), find_column(p.lexpos(1)))


def p_if_else_statement(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
                 | IF LPAREN expression RPAREN LBRACE statements RBRACE'''
    if len(p) == 12:
        p[0] = ('if-else', p[3], p[6], p[10], p.lineno(1), find_column(p.lexpos(1)))
    else:
        p[0] = ('if', p[3], p[6], p.lineno(1), find_column(p.lexpos(1)))

def p_for_loop(p):
    '''statement : FOR LPAREN statement SEMI expression SEMI statement RPAREN LBRACE statements RBRACE
                 | FOR LPAREN type_specifier IDENTIFIER IN expression RPAREN LBRACE statements RBRACE'''
    if len(p) == 12:
        p[0] = ('for_loop', 'classic', p[3], p[5], p[7], p[10], p.lineno(1), find_column(p.lexpos(1)))
    else:
        p[0] = ('for_loop', 'iterator', p[3], p[4], p[6], p[9], p.lineno(1), find_column(p.lexpos(1)))

# For 'while' loops
def p_while_loop(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE'
    p[0] = ('while_loop', p[3], p[6], p.lineno(1), find_column(p.lexpos(1)))

# For your custom 'do while' loops
def p_do_while_loop(p):
    'statement : WHILE LPAREN expression RPAREN COLON expression LBRACE statements RBRACE'
    p[0] = ('do_while_loop', p[3], p[8], p[6], p.lineno(1), find_column(p.lexpos(1)))


def p_switch_statement(p):
    '''statement : SWITCH LPAREN expression RPAREN LBRACE case_statements RBRACE'''
    p[0] = ('switch', p[3], p[6], p.lineno(1), find_column(p.lexpos(1)))

def p_case_statements(p):
    '''case_statements : CASE expression COLON statements case_statements
                       | DEFAULT COLON statements
                       | '''
    if len(p) == 6:
        p[0] = [('case', p[2], p[4], p.lineno(1), find_column(p.lexpos(1)))] + p[5]
    elif len(p) == 4:
        p[0] = [('default', 0, p[3], p.lineno(1), find_column(p.lexpos(1)))]
    else:
        p[0] = []

def p_break_statement(p):
    'statement : BREAK SEMI'
    p[0] = ('break', p.lineno(1), find_column(p.lexpos(1)))

def p_list_literal(p):
    '''expression : LBRACKET elements RBRACKET
                  | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ('list_literal', p[2], p.lineno(1), find_column(p.lexpos(1)))
    else:
        p[0] = ('list_literal', [], p.lineno(1), find_column(p.lexpos(1)))

def p_elements(p):
    '''elements : expression COMMA elements
                | expression'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expression_index(p):
    'expression : expression LBRACKET expression RBRACKET'
    p[0] = ('index_access', p[1], p[3], p.lineno(1), find_column(p.lexpos(1)))

def p_list_operation(p):
    '''list_operation : IDENTIFIER LBRACKET expression RBRACKET EQUALS expression
                      | IDENTIFIER LBRACKET expression RBRACKET LARROW expression
                      | IDENTIFIER MINUSEQ LBRACKET expression RBRACKET'''
    if p[5] == '=':
        p[0] = ('modify_by_index', p[1], p[3], p[6], p.lineno(1), find_column(p.lexpos(1)))
    elif p[5] == '<-':
        p[0] = ('list_insert', p[1], p[3], p[6], p.lineno(1), find_column(p.lexpos(1)))
    elif p[2] == '-=':
        p[0] = ('remove_index', p[1], p[4], p.lineno(1), find_column(p.lexpos(1)))

def p_list_find(p):
    'expression : IDENTIFIER AT expression'
    p[0] = ('list_find', p[1], p[3], p.lineno(1), find_column(p.lexpos(1)))

def p_declaration(p):
    '''declaration : type_specifier IDENTIFIER EQUALS expression'''
    p[0] = ('declare', p[1], p[2], p[4], p.lineno(1), find_column(p.lexpos(1)))

def p_type_specifier(p):
    '''type_specifier : INT
                     | FLOAT
                     | BOOL
                     | STR
                     | UNTYPED
                     | VOID
                     | LIST LT type_specifier GT'''
    if len(p) == 5:
        p[0] = f"LIST<{p[3]}>"
    else:
        p[0] = keywords.get(p[1], p[1])




def p_assignment(p):
    '''assignment : IDENTIFIER EQUALS expression
                  | IDENTIFIER double_operation expression'''
    if p[2] in ["+=", "-=", "*=", "/="]:
        p[0] = ('double_operation', p[1], p[2], p[3], p.lineno(1), find_column(p.lexpos(1)))
    else:
        p[0] = ('assign', p[1], p[3], p.lineno(1), find_column(p.lexpos(1)))

def p_double_operation(p):
    '''double_operation : PLUSEQ
                        | MINUSEQ
                        | MULEQ
                        | DIVEQ'''
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression'''
    p[0] = ('binop', p[2], p[1], p[3], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_number(p):
    'expression : INTEGER_LITERAL'
    p[0] = ('number', p[1], p.lineno(1), find_column(p.lexpos(1)))


def p_expression_negative_number(p):
    'expression : MINUS INTEGER_LITERAL'
    p[0] = ('number', -p[2], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_float(p):
    'expression : FLOAT_LITERAL'
    p[0] = ('float', p[1], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_negative_float(p):
    'expression : MINUS FLOAT_LITERAL'
    p[0] = ('float', -p[2], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_boolean(p):
    '''expression : TRUE
                  | FALSE'''
    p[0] = ('boolean', p[1], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_string(p):
    'expression : STRING_LITERAL'
    p[0] = ('string', p[1], p.lineno(1), find_column(p.lexpos(1)))


def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = ('identifier', p[1], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_compare(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression
                  | expression GE expression
                  | expression LE expression
                  | expression NE expression'''
    p[0] = ('compare', p[2], p[1], p[3], p.lineno(1), find_column(p.lexpos(1)))

def p_expression_not(p):
    'expression : EXCLAMATION expression'
    p[0] = ('not', p[2], p.lineno(1), find_column(p.lexpos(1)))

def p_expression(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression_cast(p):
    '''expression : expression RARROW type_specifier'''
    p[0] = ('casting', p[1], p[3])
    

def p_error(p):
    if p:
        print(f"Syntax error at line {p.lineno}, position {p.lexpos}: Unexpected {p.type} -> {p.value}")
    else:
        print("Syntax error: Unexpected end of file")


parser = yacc.yacc() 