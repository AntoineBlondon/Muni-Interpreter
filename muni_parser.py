from ply import yacc
from muni_lexer import tokens, keywords 
from muni_ast_nodes import *

precedence = (
    ('right', 'RARROW'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('left', 'AMPERSAND', 'PIPE'),
    ('right', 'EXCLAMATION'),
    ('left', 'SEMI')
    
)

def p_program(p):
    'program : statements'
    p[0] = StatementList(statements=p[1], lineno=p.lineno(1))

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
                 | module_declaration
                 | return_statement SEMI
                 | import_statement SEMI
                 | emit_statement SEMI
                 | signal_declaration SEMI
                 | when_statement
                 | watch_statement
                 | throw_statement SEMI'''
    p[0] = p[1]


def p_type_specifier(p):
    '''type_specifier : BOOLEAN
                      | INT
                      | FLOAT
                      | COMPLEX
                      | STRING
                      | VOID
                      | UNTYPED
                      | LIST
                      | LIST IMPORT_LITERAL
                      | DICT
                      | DICT LT type_specifier COMMA type_specifier GT'''
    if len(p) == 3:
        if p[1] == 'list':
            p[0] = ('list', p[2])
    elif len(p) == 7:
        if p[1] == 'dict':
            p[0] = ('dict', p[3], p[5])
    elif p[1] == 'list':
        p[0] = ('list', 'UNTYPED')
    elif p[1] == 'dict':
        p[0] = ('dict', 'UNTYPED', 'UNTYPED')
    else:
        p[0] = p[1]


def p_list_initialization(p):
    '''expression : LBRACKET list_elements RBRACKET
                  | LBRACKET RBRACKET'''
    if len(p) == 4:
        p[0] = ListInitialization(elements=p[2], lineno=p.lineno(1))
    else:
        p[0] = ListInitialization(elements=[], lineno=p.lineno(1))

def p_list_elements(p):
    '''list_elements : list_elements COMMA expression
                     | expression'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_element_access(p):
    '''expression : expression LBRACKET expression RBRACKET'''
    p[0] = ElementAccess(expression=p[1], index=p[3], lineno=p.lineno(1))

def p_element_assignment(p):
    'assignment : expression LBRACKET expression RBRACKET EQUALS expression'
    p[0] = ElementAssignment(name=p[1], index=p[3], value=p[6], lineno=p.lineno(1))

def p_dict_initialization(p):
    '''expression : LBRACE dict_elements RBRACE
                  | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = DictInitialization(elements=p[2], lineno=p.lineno(1))
    else:
        p[0] = DictInitialization(elements={}, lineno=p.lineno(1))

def p_dict_elements(p):
    '''dict_elements : dict_elements COMMA dict_element
                     | dict_element'''
    if len(p) == 4:
        p[0] = {**p[1], **p[3]}
    else:
        p[0] = p[1]

def p_dict_element(p):
    'dict_element : expression COLON expression'
    p[0] = {p[1]: p[3]}


def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_casting(p):
    '''expression : expression RARROW type_specifier
                  | expression RARROW IDENTIFIER'''
    p[0] = Cast(to_type=p[3], expression=p[1], lineno=p.lineno(1))



def p_if_statement(p):
    '''statement : IF LPAREN expression RPAREN LBRACE statements RBRACE
                 | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
                 | IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE statement'''
    if len(p) == 8:
        p[0] = IfStatement(condition=p[3], true_block=p[6], lineno=p.lineno(1))
    elif len(p) == 12:
        p[0] = IfElseStatement(condition=p[3], true_block=p[6], false_block=p[10], lineno=p.lineno(1))
    else:
        p[0] = IfElseStatement(condition=p[3], true_block=p[6], false_block=p[9], lineno=p.lineno(1))


def p_while_statement(p):
    '''statement : WHILE LPAREN expression RPAREN LBRACE statements RBRACE
                 | WHILE LPAREN expression RPAREN COLON NUMBER LBRACE statements RBRACE'''
    if len(p) == 10:
        p[0] = WhileStatement(condition=p[3], body=p[8], nb_iterations=p[6], lineno=p.lineno(1))
    else:
        p[0] = WhileStatement(condition=p[3], body=p[6], lineno=p.lineno(1))

def p_until_statement(p):
    '''statement : UNTIL LPAREN expression RPAREN LBRACE statements RBRACE
                 | UNTIL LPAREN expression RPAREN COLON NUMBER LBRACE statements RBRACE'''
    if len(p) == 10:
        p[0] = UntilStatement(condition=p[3], body=p[8], nb_iterations=p[6], lineno=p.lineno(1))
    else:
        p[0] = UntilStatement(condition=p[3], body=p[6], lineno=p.lineno(1))


def p_for_loop(p):
    '''statement : FOR LPAREN statement statement statement RPAREN LBRACE statements RBRACE
                 | FOR LPAREN type_specifier IDENTIFIER IN expression RPAREN LBRACE statements RBRACE'''
    if "in" in p:
        p[0] = ForInStatement(type_specifier=p[3], identifier=p[4], iterable=p[6], body=p[9], lineno=p.lineno(1))
    else:
        p[0] = ForStatement(begin_statement=p[3], condition=p[4], end_statement=p[5], body=p[8], lineno=p.lineno(1))

def p_d_expression(p):
    '''expression : dot_expression'''
    p[0] = p[1]


def p_switch_statement(p):
    '''statement : SWITCH LPAREN expression RPAREN LBRACE case_clauses RBRACE'''
    if len(p) == 9:
        p[0] = SwitchStatement(expression=p[3], cases=p[6], default_case=p[7], lineno=p.lineno(1))
    else:
        p[0] = SwitchStatement(expression=p[3], cases=p[6], default_case=None, lineno=p.lineno(1))

def p_case_clauses(p):
    '''case_clauses : case_clauses case_clause
                    | case_clause'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_case_clause(p):
    'case_clause : CASE expression COLON statements BREAK SEMI'
    p[0] = CaseClause(value=p[2], statements=p[4], lineno=p.lineno(1))

def p_default_clause(p):
    'case_clause : DEFAULT COLON statements BREAK SEMI'
    p[0] = DefaultClause(statements=p[3], lineno=p.lineno(1))


def p_declaration(p):
    '''declaration : type_specifier IDENTIFIER EQUALS expression
                   | type_specifier IDENTIFIER'''
    match list(p):
        case [_, _, specifier, name, _, expr]:
            p[0] = Declaration(type_specifier=specifier, name=name, value=expr, lineno=p.lineno(1))
        case [_, specifier, name, _, expr]:
            p[0] = Declaration(type_specifier=specifier, name=name, value=expr, lineno=p.lineno(1))
        case [_, _, specifier, name]:
            p[0] = Declaration(type_specifier=specifier, name=name, value=None, lineno=p.lineno(1))
        case [_, specifier, name]:
            p[0] = Declaration(type_specifier=specifier, name=name, value=None, lineno=p.lineno(1))


def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression'
    p[0] = Assignment(name=p[1], value=p[3], lineno=p.lineno(1))


def p_function_declaration(p):
    '''function_declaration : type_specifier IDENTIFIER LPAREN parameter_list RPAREN LBRACE statements RBRACE'''
    p[0] = FunctionDeclaration(name=p[2], return_type=p[1], parameters=p[4], body=p[7], lineno=p.lineno(1))

def p_module_declaration(p):
    '''module_declaration : MODULE IDENTIFIER LBRACE statements RBRACE'''
    p[0] = ModuleDeclaration(name=p[2], body=p[4], lineno=p.lineno(1))


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
    '''return_statement : RETURN expression
                        | RETURN'''
    if len(p) == 2:
        p[0] = Return(value=None, lineno=p.lineno(1))
    else:
        p[0] = Return(value=p[2], lineno=p.lineno(1))


def p_expression_function_call(p):
    '''expression : dot_expression LPAREN argument_list RPAREN
                  | IDENTIFIER LPAREN argument_list RPAREN'''
    p[0] = FunctionCall(name=p[1], arguments=p[3], lineno=p.lineno(1))

def p_signal_declaration(p):
    'signal_declaration : SIGNAL IDENTIFIER'
    p[0] = SignalDeclaration(signal_name=p[2], lineno=p.lineno(1))

def p_emit_statement(p):
    'emit_statement : EMIT IDENTIFIER'
    p[0] = EmitStatement(signal_name=p[2], lineno=p.lineno(1))

def p_watch_statement(p):
    'watch_statement : WATCH LPAREN IDENTIFIER RPAREN LBRACE statements RBRACE'
    p[0] = WatchStatement(variable_name=p[3], statements=p[6], lineno=p.lineno(1))

def p_when_statement(p):
    '''when_statement : WHEN LPAREN IDENTIFIER RPAREN LBRACE statements RBRACE'''
    p[0] = WhenStatement(signal_name=p[3], statements=p[6], lineno=p.lineno(1))

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
    '''import_statement : IMPORT IMPORT_LITERAL
                        | IMPORT IMPORT_LITERAL AS IDENTIFIER'''
    if len(p) == 5:
        p[0] = ImportStatement(module_path=p[2], as_name=p[4], lineno=p.lineno(1))
    else:
        p[0] = ImportStatement(module_path=p[2], lineno=p.lineno(1))


def p_expression_dot(p):
    '''dot_expression : IDENTIFIER DOT IDENTIFIER'''
    p[0] = DotAccess(container=p[1], attribute=p[3], lineno=p.lineno(1))


def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MUL expression
                  | expression DIV expression
                  | expression MODULUS expression'''
    p[0] = BinaryOperation(left=p[1], operator=p[2], right=p[3], lineno=p.lineno(1))

def p_expression_assignment(p):
    '''expression : IDENTIFIER PLUSEQ expression
                 | IDENTIFIER MINUSEQ expression
                 | IDENTIFIER MULEQ expression
                 | IDENTIFIER DIVEQ expression
                 | IDENTIFIER MODEQ expression'''
    p[0] = ExpressionAssignment(name=p[1], operator=p[2], value=p[3], lineno=p.lineno(1))


def p_expression_logical(p):
    '''expression : expression AMPERSAND expression
                  | expression PIPE expression
                  | expression HAT expression'''
    p[0] = LogicalOperation(left=p[1], operator=p[2], right=p[3], lineno=p.lineno(1))

def p_expression_comparison(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression EQ expression
                  | expression GE expression
                  | expression LE expression
                  | expression NE expression'''
    p[0] = ComparisonOperation(left=p[1], operator=p[2], right=p[3], lineno=p.lineno(1))

def p_expression_not(p):
    'expression : EXCLAMATION expression'
    p[0] = NotOperation(operand=p[2], lineno=p.lineno(1))

def p_expression_number(p):
    '''expression : NUMBER
                  | IMAGINARY_NUMBER'''
    p[0] = Number(value=p[1], lineno=p.lineno(1))

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = Boolean(value=p[1], lineno=p.lineno(1))

def p_expression_string(p):
    'expression : STRING_LITERAL'
    p[0] = String(value=p[1], lineno=p.lineno(1))

def p_expression_identifier(p):
    'expression : IDENTIFIER'
    p[0] = Variable(name=p[1], lineno=p.lineno(1))

def p_expression_negative(p):
    'expression : MINUS expression'
    p[0] = UnaryOperation(operand=p[2], lineno=p.lineno(1))

def p_expression_argument(p):
    'expression : DOLLAR NUMBER'
    p[0] = ArgumentGet(index=p[2], lineno=p.lineno(1))


def p_range_operator(p):
    '''range_operator : RANGE_OP
                      | RANGE_OP_INCLUSIVE'''
    p[0] = p[1]

def p_expression_range(p):
    '''expression : expression range_operator expression
                  | expression range_operator expression COLON expression'''
    start = p[1]
    end = p[3]
    if len(p) == 4:
        step = 1
    else:
        step = p[5]
    p[0] = Range(start, end, step, inclusive=p[2]=="...", lineno=p.lineno(1))


def p_error(p):
    if p:
        print(f"Syntax error at {p.lineno}, illegal character {p.value}")
    else:
        print("Syntax error at EOF")


def p_throw_statement(p):
    'throw_statement : THROW expression'
    p[0] = ThrowStatement(expression=p[2], lineno=p.lineno(1))


parser = yacc.yacc()


def parse_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return parser.parse(content) 



def find_column(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column
