from ply import yacc
from muni_lexer import tokens, keywords 
from muni_ast_nodes import *

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'AMPERSAND', 'PIPE'),
    ('right', 'EXCLAMATION'),
    ('left', 'SEMI')
    
)

def p_program(p):
    'program : statements'
    p[0] = StatementList(statements=p[1])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        # If there's more than one statement, append it to the list
        p[0] = p[1] + [p[2]]
    else:
        # Single statement
        p[0] = [p[1]]

def p_statement(p):
    '''statement : expression SEMI
                 | declaration SEMI
                 | assignment SEMI
                 | function_declaration
                 | return_statement SEMI
                 | import_statement SEMI
                 | emit_statement SEMI
                 | signal_declaration SEMI
                 | when_statement
                 | watch_statement'''
    p[0] = p[1]


def p_type_specifier(p):
    '''type_specifier : BOOLEAN
                      | INT
                      | FLOAT
                      | BASED
                      | COMPLEX
                      | STRING
                      | VOID
                      | UNTYPED
                      | LIST
                      | LIST IMPORT_LITERAL'''
    if len(p) == 3:
        p[0] = ('list', p[2])
    elif p[1] == 'list':
        p[0] = ('list', 'UNTYPED')
    else:
        p[0] = p[1]


def p_list_initialization(p):
    '''expression : LBRACKET list_elements RBRACKET
                  | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ListInitialization(elements=p[2])
    else:
        p[0] = ListInitialization(elements=[])

def p_list_elements(p):
    '''list_elements : list_elements COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_list_access(p):
    'expression : IDENTIFIER LBRACKET expression RBRACKET'
    p[0] = ListAccess(name=p[1], index=p[3])

def p_list_assignment(p):
    'assignment : IDENTIFIER LBRACKET expression RBRACKET EQUALS expression'
    p[0] = ListAssignment(name=p[1], index=p[3], value=p[6])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_casting(p):
    'expression : type_specifier RARROW expression'
    p[0] = Cast(to_type=p[1], expression=p[3])



def p_if_statement(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statements RBRACE
                 | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
                 | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE statement'''
    if len(p) == 8:
        p[0] = IfStatement(condition=p[3], true_block=p[6])
    elif len(p) == 12:
        p[0] = IfElseStatement(condition=p[3], true_block=p[6], false_block=p[10])
    else:
        p[0] = IfElseStatement(condition=p[3], true_block=p[6], false_block=p[9])


def p_while_statement(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE
                 | WHILE LPAREN expression RPAREN COLON NUMBER LBRACE statements RBRACE'''
    if len(p) == 10:
        p[0] = WhileStatement(condition=p[3], body=p[8], nb_iterations=p[6])
    else:
        p[0] = WhileStatement(condition=p[3], body=p[6])

def p_until_statement(p):
    '''statement : UNTIL LPAREN expression RPAREN LBRACE statements RBRACE
                 | UNTIL LPAREN expression RPAREN COLON NUMBER LBRACE statements RBRACE'''
    if len(p) == 10:
        p[0] = UntilStatement(condition=p[3], body=p[8], nb_iterations=p[6])
    else:
        p[0] = UntilStatement(condition=p[3], body=p[6])


def p_for_loop(p):
    '''statement : FOR LPAREN statement statement statement RPAREN LBRACE statements RBRACE
                 | FOR LPAREN type_specifier IDENTIFIER IN expression RPAREN LBRACE statements RBRACE'''
    if "in" in p:
        p[0] = ForInStatement(type_specifier=p[3], identifier=p[4], iterable=p[6], body=p[9])
    else:
        p[0] = ForStatement(begin_statement=p[3], condition=p[4], end_statement=p[5], body=p[8])




def p_switch_statement(p):
    '''statement : SWITCH LPAREN expression RPAREN LBRACE case_clauses RBRACE'''
    if len(p) == 9:
        p[0] = SwitchStatement(expression=p[3], cases=p[6], default_case=p[7])
    else:
        p[0] = SwitchStatement(expression=p[3], cases=p[6], default_case=None)

def p_case_clauses(p):
    '''case_clauses : case_clauses case_clause
                    | case_clause'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_case_clause(p):
    'case_clause : CASE expression COLON statements BREAK SEMI'
    p[0] = CaseClause(value=p[2], statements=p[4])

def p_default_clause(p):
    'case_clause : DEFAULT COLON statements BREAK SEMI'
    p[0] = DefaultClause(statements=p[3])


def p_declaration(p):
    '''declaration : type_specifier IDENTIFIER EQUALS expression
                   | type_specifier IDENTIFIER'''
    if len(p) == 5:
        # Declaration with assignment
        p[0] = Declaration(type_specifier=p[1], name=p[2], value=p[4])
    else:
        # Declaration without assignment
        p[0] = Declaration(type_specifier=p[1], name=p[2], value=None)


def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression'
    p[0] = Assignment(name=p[1], value=p[3])


def p_function_declaration(p):
    '''function_declaration : type_specifier IDENTIFIER LPAREN parameter_list RPAREN LBRACE statements RBRACE'''
    p[0] = FunctionDeclaration(name=p[2], return_type=p[1], parameters=p[4], body=p[7])

def p_parameter_list(p):
    '''parameter_list : parameter_list COMMA type_specifier IDENTIFIER
                      | type_specifier IDENTIFIER
                      | '''
    if len(p) == 5:
        p[0] = p[1] + [(p[3], p[4])]
    elif len(p) == 3:
        p[0] = [(p[1], p[2])]
    else:
        p[0] = []

def p_return_statement(p):
    'return_statement : RETURN expression'
    p[0] = Return(value=p[2])


def p_expression_function_call(p):
    'expression : IDENTIFIER LPAREN argument_list RPAREN'
    p[0] = FunctionCall(name=p[1], arguments=p[3])

def p_signal_declaration(p):
    'signal_declaration : SIGNAL IDENTIFIER'
    p[0] = SignalDeclaration(signal_name=p[2])

def p_emit_statement(p):
    'emit_statement : EMIT IDENTIFIER'
    p[0] = EmitStatement(signal_name=p[2])

def p_watch_statement(p):
    'watch_statement : WATCH LPAREN IDENTIFIER RPAREN LBRACE statements RBRACE'
    p[0] = WatchStatement(variable_name=p[3], statements=p[6])

def p_when_statement(p):
    '''when_statement : WHEN LPAREN IDENTIFIER RPAREN LBRACE statements RBRACE'''
    p[0] = WhenStatement(signal_name=p[3], statements=p[6])

def p_argument_list(p):
    '''argument_list : argument_list COMMA expression
                     | expression
                     | '''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []


def p_import_statement(p):
    '''import_statement : IMPORT IMPORT_LITERAL'''
    p[0] = ImportStatement(module_path=p[2])



def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression MODULUS expression'''
    p[0] = BinaryOperation(left=p[1], operator=p[2], right=p[3])

def p_expression_assignment(p):
    '''expression : IDENTIFIER PLUSEQ expression
                 | IDENTIFIER MINUSEQ expression
                 | IDENTIFIER MULEQ expression
                 | IDENTIFIER DIVEQ expression
                 | IDENTIFIER MODEQ expression'''
    p[0] = ExpressionAssignment(name=p[1], operator=p[2], value=p[3])


def p_expression_logical(p):
    '''expression : expression AMPERSAND expression
                  | expression PIPE expression
                  | expression HAT expression'''
    p[0] = LogicalOperation(left=p[1], operator=p[2], right=p[3])

def p_expression_comparison(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression
                  | expression GE expression
                  | expression LE expression
                  | expression NE expression'''
    p[0] = ComparisonOperation(left=p[1], operator=p[2], right=p[3])

def p_expression_not(p):
    'expression : EXCLAMATION expression'
    p[0] = NotOperation(operand=p[2])

def p_expression_number(p):
    '''expression : NUMBER
                  | IMAGINARY_NUMBER
                  | BASED_NUMBER'''
    p[0] = Number(value=p[1])

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = Boolean(value=p[1])

def p_expression_string(p):
    'expression : STRING_LITERAL'
    p[0] = String(value=p[1])

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = Variable(name=p[1])


def p_error(p):
    if p:
        print(f"Syntax error at {p.lineno}, illegal character {p.value}")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return parser.parse(content) 

