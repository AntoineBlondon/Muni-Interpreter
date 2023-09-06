from native_functions import *
from munilexer import lexer
from muniparser import parser

class RuntimeContext:
    def __init__(self):
        self.symbol_table = {}
        self.function_table = {}
        self.main_ast = []
        self.imported_files = []
    
    def parse_import(self, file_path, namespace):
        if file_path in self.imported_files:
            return []
        self.imported_files.append(file_path)
        file_content = read_file(file_path)
        lexer.input(file_content)
        ast = parser.parse(file_content, lexer=lexer)
        return add_namespace(ast, namespace)



    def run_ast(self, ast, context=None, args=[], location="./"):
        if context is None:
            context = ExecutionASTContext(args=args, location=location)
        context.function_table = self.function_table
        if(context.debug): print(f"Running AST: {ast} with local scope: {context.local_scope}")
        if isinstance(ast, list):
            for stmt in ast:
                self.run_ast(stmt, context)
            return

        try:
            if ast is None:
                return None

            node_type = ast[0]
            lineno = ast[-2] if len(ast) > 2 and type(ast[-2]) == int else "unknown"
            lexpos = ast[-1] if len(ast) > 1 and type(ast[-1]) == int else "unknown"
            if lineno != "unknown" and lexpos != "unknown": ast = ast[:-2]

            if node_type in ['binop', 'number', 'float', 'boolean', 'string','list_literal', 'identifier', 'compare', 'casting']:
                return self.evaluate_expression(ast, context)
            elif node_type in ['declare', 'assign', 'double_operation']:
                return self.manage_variable(ast, context)
            elif node_type in ['if', 'if-else', 'for_loop', 'while_loop', 'do_while_loop', 'switch']:
                return self.control_flow(ast, context)
            elif node_type in ['function_declaration', 'function_call']:
                return self.manage_function(ast, context)
            elif node_type in ['index_access', 'modify_by_index', 'list_insert', 'list_find', 'remove_index']:
                return self.list_operations(ast, context)
            elif node_type in ['return', 'break', 'import']:
                return self.special_constructs(ast, context)
            else:
                print(f"Unknown node type: {node_type}")


        except BreakException:
            raise
        except ReturnException as e:
            raise e
        except Exception as e:
            print(f"Runtime error at line {lineno}, column {lexpos}: {e}")







    def evaluate_expression(self, ast, context):
        node_type = ast[0]

        if node_type == 'binop':
            _, op, left, right = ast
            left_value = self.run_ast(left, context)
            right_value = self.run_ast(right, context)

            left_type = type(left_value).__name__.upper()
            right_type = type(right_value).__name__.upper()
            
            if op == '+':
                return add(left_value, right_value)
            elif op == '-':
                return substract(left_value, right_value)
            elif op == '*':
                return multiply(left_value, right_value)
            elif op == '/':
                return divide(left_value, right_value)
        elif node_type == 'compare':
            _, op, left, right = ast
            left_value = self.run_ast(left, context)
            right_value = self.run_ast(right, context)

            left_type = type(left_value).__name__.upper()
            right_type = type(right_value).__name__.upper()

            if left_type != right_type:
                raise TypeError(f"Type mismatch: {left_type} and {right_type} for operator {op}")

            if op == '>':
                return left_value > right_value
            elif op == '<':
                return left_value < right_value
            elif op == '==':
                return left_value == right_value
            elif op == '>=':
                return left_value >= right_value
            elif op == '<=':
                return left_value <= right_value
            elif op == '!=':
                return left_value != right_value

        elif node_type == 'number':
            return ast[1]
        
        elif node_type == 'float':
            return ast[1]

        elif node_type == 'boolean':
            return ast[1]

        elif node_type == 'string':
            return ast[1]
        elif node_type == 'list_literal':
            _, elements = ast
            list_value = [self.run_ast(element, context) for element in elements]
            return list_value
        elif node_type == 'identifier':
            return context.local_scope.get(ast[1], self.symbol_table.get(ast[1], None))['value']
        elif node_type == 'casting':
            _, expr, type_to_cast = ast
            value = self.run_ast(expr, context)
            value = cast(value, type_to_cast)
            return value
        

    def manage_variable(self, ast, context):
        node_type = ast[0]

        if node_type == 'declare':
            _, var_type, var_name, elements = ast
            if var_type.startswith("LIST"):
                list_value = self.run_ast(elements, context)
                check_type(list_value, var_type)
                if context.is_local:
                    context.local_scope[var_name] = {'type': var_type, 'value': list_value}
                    
                else:
                    self.symbol_table[var_name] = {'type': var_type, 'value': list_value}
            else:
                value = self.run_ast(elements, context)
                check_type(value, var_type)
                if context.is_local:
                    context.local_scope[var_name] = {'type': var_type, 'value': value}
                else:
                    self.symbol_table[var_name] = {'type': var_type, 'value': value}

        elif node_type == 'assign':
            _, var_name, expr = ast
            value = self.run_ast(expr, context)
            var_info = context.local_scope.get(var_name, self.symbol_table.get(var_name, None))
            if var_info is None:
                raise KeyError(f"Variable {var_name} not declared")
            check_type(value, var_info['type'])
            var_info['value'] = value

        elif node_type == 'double_operation':
            _, var_name, op, expr = ast
            value = self.run_ast(expr, context)
            var_info = context.local_scope.get(var_name, self.symbol_table.get(var_name, None))
            if var_info is None:
                raise KeyError(f"Variable {var_name} not declared")
            check_type(value, var_info['type'])
            if op == "+=":
                var_info['value'] = add(var_info['value'], value)
            elif op == "-=":
                var_info['value'] = var_info['value'] - value
            elif op == "*=":
                var_info['value'] = var_info['value'] * value
            elif op == "/=":
                var_info['value'] = var_info['value'] / value

    def control_flow(self, ast, context):
        node_type = ast[0]
        if node_type == 'if':
            condition, true_block = ast[1], ast[2]
            condition_value = self.run_ast(condition, context)
            if condition_value:
                self.run_ast(true_block, context)

        elif node_type == 'if-else':
            condition, true_block, false_block = ast[1], ast[2], ast[3]
            condition_value = self.run_ast(condition, context)
            if condition_value:
                self.run_ast(true_block, context)
            else:
                self.run_ast(false_block, context)
        elif node_type == 'for_loop':
            loop_type, *loop_parts = ast[1:]
            if loop_type == 'classic':
                init, condition, update, body = loop_parts
                self.run_ast(init, context)
                try:
                    while self.run_ast(condition, context):
                        self.run_ast(body, context)
                        self.run_ast(update, context)
                except BreakException:
                    pass
            elif loop_type == 'iterator':
                iter_type, iter_var, iter_list, body = loop_parts
                list_value = self.run_ast(iter_list, context)
                if not isinstance(list_value, list):
                    raise TypeError(f"Expected a list for iteration, got {type(list_value).__name__}")
                try:
                    for element in list_value:
                        check_type(element, iter_type)
                        if context.is_local:
                            context.local_scope[iter_var] = {'type': iter_type, 'value': element}
                        else:
                            self.symbol_table[iter_var] = {'type': iter_type, 'value': element}
                        self.run_ast(body, context)
                except BreakException:
                    pass



        elif node_type == 'while_loop':
            _, condition, body = ast
            try:
                while self.run_ast(condition, context):
                    self.run_ast(body, context)
            except BreakException:
                pass

        # For your custom 'do while' loops
        elif node_type == 'do_while_loop':
            _, condition, body, num_of_iteration = ast
            if(not isinstance(num_of_iteration, int)):
                num_of_iteration = self.run_ast(num_of_iteration, context)
            try:
                for i in range(num_of_iteration):
                    self.run_ast(body, context)
                while self.run_ast(condition, context):
                    self.run_ast(body, context)
            except BreakException:
                pass
        elif node_type == 'switch':
            try:
                _, switch_expr, case_statements = ast
                switch_value = self.run_ast(switch_expr, context)
                
                executed_case = False
                for case_type, case_value, case_body, a, b in case_statements:
                    
                    if case_type == 'case':
                        case_eval_value = self.run_ast(case_value, context)
                        if switch_value == case_eval_value:
                            self.run_ast(case_body, context)
                            executed_case = True
                            break
                    elif case_type == 'default' and not executed_case:
                        self.run_ast(case_body, context)
                        break
            except BreakException:
                pass
        

    def manage_function(self, ast, context):
        node_type = ast[0]
        if node_type == 'function_declaration':
            _, func_type, func_name, params, func_body, default_return = ast
            self.function_table[func_name] = (func_type, params, func_body, default_return)
            if(context.debug): print(f"Debug: Declaring function {func_name} with parameters {params}")
            if default_return is not None:
                check_type(self.run_ast(default_return, context), func_type)

        elif node_type == 'function_call':
            _, func_name, args = ast
            if func_name in native_functions:
                if(context.debug): print(f"Debug: Calling native function {func_name} with arguments {args}")
                return call_native_function(func_name, args, self.run_ast, self.symbol_table, context)
            if(context.debug): print(f"Debug: Calling function {func_name} with arguments {args} and parameters {params}")
            func_type, params, func_body, default_return = self.function_table.get(func_name, (None, [], [], None))
            for (param_type, param_name), arg in zip(params, args):
                arg_value = self.run_ast(arg, context)
                if(context.debug): print(f"Debug: Argument value is {arg_value} for parameter {param_name} of type {param_type}")
                check_type(arg_value, param_type)
            

            if len(params) != len(args):
                print(f"Error: Argument count mismatch in function {func_name}.")
                return

            new_local_scope = context.local_scope.copy()
            #print(f"params: {params}")
            
            new_local_scope.update({param[1]: {'type': param[0], 'value': self.run_ast(arg, context) }for param, arg in zip(params, args)})
            #print(f"new local scope: {new_local_scope}")

            try:
                context.local_scope = new_local_scope
                context.is_local = True
                context.expected_return_type = func_type
                self.run_ast(func_body, context)
            except ReturnException as e:
                return e.value

            # If the function body didn't return, use the default return value
            return self.run_ast(default_return, context)

    def list_operations(self, ast, context):
        node_type = ast[0]
        if node_type == 'index_access':
            list_ast, index_ast = ast[1], ast[2]
            list_value = self.run_ast(list_ast, context)
            index_value = self.run_ast(index_ast, context)
            if index_value < 0:
                index_value += len(list_value)
            if not isinstance(list_value, list) and not isinstance(list_value, str):
                raise TypeError("Index access on non-list type")
            if not isinstance(index_value, int):
                raise TypeError("List index must be an integer")
            try:
                return list_value[index_value]
            except IndexError:
                raise IndexError("List index out of range")
        elif node_type == 'modify_by_index':
            list_ast, index_ast, value_ast = ast[1], ast[2], ast[3]
            list_value = context.local_scope.get(list_ast, self.symbol_table.get(list_ast, None))['value']
            index_value = self.run_ast(index_ast, context)
            new_value = self.run_ast(value_ast, context)

            if index_value < 0:
                index_value += len(list_value)
            
            if not isinstance(list_value, list):
                raise TypeError("Index access on non-list type")
            if not isinstance(index_value, int):
                raise TypeError("List index must be an integer")
            
            try:
                list_value[index_value] = new_value
            except IndexError:
                raise IndexError("List index out of range")
        elif node_type == 'list_insert':
            list_name, index_expr, value_expr = ast[1], ast[2], ast[3]
            index = self.run_ast(index_expr, context)
            value = self.run_ast(value_expr, context)
            list_value = context.local_scope.get(list_name, self.symbol_table.get(list_name, None))['value']
            list_value.insert(index, value)
        elif node_type == 'list_find':
            list_name, value_expr = ast[1], ast[2]
            value = self.run_ast(value_expr, context)
            list_value = context.local_scope.get(list_name, self.symbol_table.get(list_name, None))['value']
            return list_value.index(value)
        elif node_type == 'remove_index':
            list_name, value_expr = ast[1], ast[2]
            to_remove = self.run_ast(value_expr, context)
            list_value = context.local_scope.get(list_name, self.symbol_table.get(list_name, None))['value']
            if(isinstance(list_value, str)):
                #remove char at index
                return list_value[:to_remove] + list_value[to_remove+1:]
            return list_value.pop(to_remove)
        
            

    def special_constructs(self, ast, context):
        node_type = ast[0]
        if node_type == 'break':
            raise BreakException()
        elif node_type == 'return':
            _, expr = ast
            value = self.run_ast(expr, context)
            check_type(value, context.expected_return_type)
            raise ReturnException(value)
        elif node_type == 'import':
            if len(ast) == 2:
                _, file_path = ast
                if(not isinstance(file_path, str)):
                    file_path = self.run_ast(file_path, context)
                namespace = file_path.split('/')[-1].split('.')[0]
            else:
                _, file_path, namespace = ast
                if(not isinstance(file_path, str)):
                    file_path = self.run_ast(file_path, context)
            if file_path in self.imported_files:
                return
            
            imported_ast = self.parse_import(file_path, namespace)
            global main_ast
            main_ast = merge_asts(main_ast, imported_ast)
            
            self.run_ast(main_ast, context)






def check_type(value, expected_type):
    actual_type = type(value).__name__.upper()
    if expected_type == '?': return
    if actual_type == "NONE":
        raise TypeError(f"Type cannot be NONE")
    if (actual_type == 'LIST' and not expected_type.startswith('LIST')) and actual_type != expected_type:
        raise TypeError(f"Expected {expected_type}, got {actual_type}")
    
    if  expected_type.startswith('LIST'):
        expected_element_type = expected_type.split("LIST")[1][1:-1]
        if expected_element_type == '?': return

        if expected_element_type is not None:
            for element in value:
                actual_element_type = type(element).__name__.upper()
                if actual_element_type != expected_element_type:
                    raise TypeError(f"Expected element type {expected_element_type}, got {actual_element_type}")





def cast(value, type_to_cast):
    # Remove leading/trailing white spaces from type specifier

    type_to_cast = type_to_cast.strip().lower()

    # Determine the type of the value
    value_type = type(value).__name__.lower()

    if value_type == type_to_cast:
        # If the value is already of the type specified, return it as is.
        return value

    try:
        if type_to_cast == 'int':
            return int(value)
        elif type_to_cast == 'bool':
            return bool(value)
        elif type_to_cast == 'str':
            return str(value)
        elif type_to_cast == 'float':
            return float(value)
        else:
            raise ValueError(f"Unsupported type to cast: {type_to_cast}")
    except (ValueError, TypeError):
        raise TypeError(f"Cannot cast {value} from {value_type} to {type_to_cast}")



def add_namespace(ast, namespace):
    new_ast = []
    for node in ast:
        node_type = node[0]
        if node_type == 'function_declaration':
            _, func_type, func_name, params, func_body, default_return, a, b = node
            new_func_name = f"{namespace}|{func_name}" if func_name not in native_functions else func_name
            new_func_body = add_namespace(func_body, namespace)
            new_node = ('function_declaration', func_type, new_func_name, params, new_func_body, default_return)
            new_ast.append(new_node)
        elif node_type == 'function_call':
            _, func_name, args, a, b = node
            new_func_name = f"{namespace}|{func_name}" if func_name not in native_functions else func_name
            new_node = ('function_call', new_func_name, args)
            new_ast.append(new_node)
        else:
            new_ast.append(node)
    return new_ast



def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read() 



def merge_asts(main_ast, imported_ast):
    return imported_ast + main_ast




def add(a, b):
    if isinstance(a, list) and not isinstance(b, list):
        b = [b]
    elif not isinstance(a, list) and isinstance(b, list):
        a = [a]
    elif isinstance(a, str) and isinstance(b, (int, float)):
        return a + str(b)
    elif isinstance(a, (int, float)) and isinstance(b, str):
        return str(a) + b
    return a + b

def substract(a, b):
    if isinstance(a, list) and not isinstance(b, list): # [1, 2, 3, 4] - 4 = [1, 2, 3]
        if b in a:
            c = a.copy()
            c.remove(b)
            return c
        return a
    if isinstance(a, list) and isinstance(b, list): # [1, 2, 3, 4, 5] - [4, 5] = [1, 2, 3]
        c = a.copy()
        for element in b:
            c.remove(element)
        return c
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b






class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    pass

class ExecutionASTContext:
    def __init__(self, local_scope=None, is_local=False, debug=False, expected_return_type=None, args=[], location="./"):
        self.local_scope = local_scope if local_scope is not None else {}
        self.is_local = is_local
        self.debug = debug
        self.expected_return_type = expected_return_type
        self.args = args
        self.location = location
        self.function_table = {}





