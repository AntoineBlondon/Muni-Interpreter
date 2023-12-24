from muni_types import *
from muni_ast_nodes import *
import importlib
import os
import muni_parser 
import threading

class Runtime:
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}
        self.signals = {}
        self.register_stdlib_functions()

    def define_function(self, func):
        self.functions[func.name] = func

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1]

    def define_variable(self, name, value, type_specifier=None):
        if type_specifier == "?":
            self.current_scope()[name] = value
        else:
            value = self.perform_cast(type_specifier, value)
            self.check_type(type_specifier, value)
            self.current_scope()[name] = value

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable '{name}' not found")
    
    def is_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False
    
    def define_signal(self, signal_name):
        if signal_name in self.signals:
            raise Exception(f"Signal Error: {signal_name} already a signal.")
        self.signals[signal_name] = None

    def assign_signal(self, signal_name, statements):
        if signal_name not in self.signals:
            raise Exception(f"Signal Error: {signal_name} not a signal.")

        if self.signals[signal_name] is None:
            self.signals[signal_name] = [statements]
        else:
            self.signals[signal_name].append(statements)

    def emit_signal(self, signal_name):
        if signal_name not in self.signals:
            raise Exception(f"Signal Error: {signal_name} not a signal.")
        
        for statements in self.signals[signal_name]:
            thread = threading.Thread(target=self.evaluate_block, args=(statements,))
            thread.start()

    
    def evaluate(self, node, debug=False):
        if debug: print(node)
        # Handle Number nodes
        if isinstance(node, (Number, Boolean, String)):
            return node.value
        
        elif isinstance(node, Variable):
            return self.get_variable(node.name)
        
        elif isinstance(node, Declaration):
            value = self.evaluate(node.value)
            self.define_variable(node.name, value, node.type_specifier)

        elif isinstance(node, Assignment):
            value = self.evaluate(node.value)
            var_type = type(self.get_variable(node.name))
            if var_type != "UNTYPED":
                self.check_type(var_type, value)
            try:
                self.define_variable(node.name, value, str(value.symbol()))
            except Exception as e:
                self.define_variable(node.name, value, str(type(value).symbol()))

        elif isinstance(node, ExpressionAssignment): # a += 1, a -= 1, a /=1 ...
            value = self.evaluate(node.value)
            variable = self.get_variable(node.name)
            self.define_variable(node.name, self.apply_binary_operator(variable, value, node.operator[:-1]), str(variable.symbol()))



        # Handle BinaryOperation nodes
        elif isinstance(node, BinaryOperation):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            return self.apply_binary_operator(left_val, right_val, node.operator)
        
        # Handle LogicalOperation nodes
        elif isinstance(node, LogicalOperation):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            return self.apply_logical_operator(left_val, right_val, node.operator)
        
        # Handle ComparisonOperation nodes
        elif isinstance(node, ComparisonOperation):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            return self.apply_comparison_operator(left_val, right_val, node.operator)
        
        elif isinstance(node, NotOperation):
            value = self.evaluate(node.operand)
            return not value
        
        elif isinstance(node, UnaryOperation):
            value = self.evaluate(node.operand)
            return -value

        elif isinstance(node, FunctionCall):
            function = self.get_function(node.name)
            if callable(function):
                arguments = [self.evaluate(arg) for arg in node.arguments]
                return function(*arguments)
            return self.call_function(function, node.arguments)

        elif isinstance(node, Return):
            return self.evaluate(node.value)
        
        elif isinstance(node, FunctionDeclaration):
            self.define_function(node)
            return None

        elif isinstance(node, ImportStatement):
            return self.handle_import(node)

        elif isinstance(node, Muni_Type):
            return node
        
        elif isinstance(node, Cast):
            value = self.evaluate(node.expression)
            return self.perform_cast(node.to_type, value)
        
        elif isinstance(node, IfStatement):
            condition_value = self.evaluate(node.condition)
            if condition_value:
                return self.evaluate_block(node.true_block)
            return None

        elif isinstance(node, IfElseStatement):
            condition_value = self.evaluate(node.condition)
            if condition_value:
                self.evaluate_block(node.true_block)
            else:
                self.evaluate_block(node.false_block)
            return None

        elif isinstance(node, WhileStatement):
            for i in range(int(node.nb_iterations)):
                self.evaluate_block(node.body)
            while self.evaluate(node.condition):
                self.evaluate_block(node.body)
            return None
        
        elif isinstance(node, UntilStatement):
            for i in range(int(node.nb_iterations)):
                self.evaluate_block(node.body)
            while not self.evaluate(node.condition):
                self.evaluate_block(node.body)
            return None
        
        elif isinstance(node, ForInStatement):
            for value in self.evaluate(node.iterable):
                self.check_type(node.type_specifier, value)
                self.define_variable(node.identifier, value, node.type_specifier)
                self.evaluate_block(node.body)
            return None
        
        elif isinstance(node, ForStatement):
            self.evaluate(node.begin_statement)
            while self.evaluate(node.condition):
                self.evaluate_block(node.body)
                self.evaluate(node.end_statement)
            return None
        
        elif isinstance(node, SwitchStatement):
            switch_value = self.evaluate(node.expression)
            default_case = None
            for case in node.cases:
                if not isinstance(case, CaseClause):
                    default_case = case
                    continue
                if self.evaluate(case.value) == switch_value:
                    self.evaluate_block(case.statements)
                    return
            if default_case:
                self.evaluate_block(default_case.statements)

        elif isinstance(node, SignalDeclaration):
            signal_name = node.signal_name
            self.define_signal(signal_name)
            return None
        
        elif isinstance(node, EmitStatement):
            signal_name = node.signal_name
            self.emit_signal(signal_name)
        
        elif isinstance(node, WhenStatement):
            signal_name = node.signal_name
            statements = node.statements
            self.assign_signal(signal_name, statements)

        elif isinstance(node, ListInitialization):
            values = [self.evaluate(val) for val in node.elements]
            return Muni_List(values)

        elif isinstance(node, ListAccess):
            list_object = self.evaluate(node.expression)
            index = self.evaluate(node.index)
            return list_object.get_item(index)
    
        elif isinstance(node, ListAssignment):
            list_object = self.evaluate(node.name)
            index = self.evaluate(node.index)
            value = self.evaluate(node.value)
            list_object.set_item(index, value)
            self.define_variable(node.name, list_object, str(list_object.symbol()))

        elif self.is_variable(node):
            return self.get_variable(node)
        
        elif node is None:
            return None
        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def apply_binary_operator(self, left, right, operator):
        
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if (right == 0):
                raise Exception("Division by zero")
            
            return left / right
        elif operator == '%':
            return left % right
        else:
            raise Exception(f"Unknown binary operator: {operator}")
        
    def apply_logical_operator(self, left, right, operator):
        if operator == '&':
            return left and right
        elif operator == '|':
            return left or right
        elif operator == '^':
            return left ^ right
        else:
            raise Exception(f"Unknown logical operator: {operator}")
    
    def apply_comparison_operator(self, left, right, operator):
        if operator == '>':
            return left > right
        elif operator == '<':
            return left < right
        elif operator == '==':
            return left == right
        elif operator == '>=':
            return left >= right
        elif operator == '<=':
            return left <= right
        elif operator == '!=':
            return left != right
        else:
            raise Exception(f"Unknown comparison operator: {operator}")
        
    def check_type(self, type_specifier, value):
        if type_specifier == 'int':
            if not isinstance(value, Muni_Int):
                raise Exception(f"Expected an int, got {type(value)}")
        elif type_specifier == 'float':
            if not isinstance(value, Muni_Float):
                raise Exception(f"Expected a float, got {type(value)}")
        elif type_specifier == 'complex':
            if not isinstance(value, Muni_Complex):
                raise Exception(f"Expected a complex number, got {type(value)}")
        elif type_specifier == 'boolean':
            if not isinstance(value, Muni_Boolean):
                raise Exception(f"Expected a boolean, got {type(value)}")

    def get_function(self, name):
        return self.functions.get(name, None)

    def call_function(self, function, arguments):
        # Push a new scope
        self.push_scope()

        # Assign arguments to parameters in the new scope
        for (param_type, param_name), arg in zip(function.parameters, arguments):
            self.define_variable(param_name, self.evaluate(arg), param_type)

        # Execute each statement in the function body
        result = None
        for stmt in function.body:
            if isinstance(stmt, Return):
                result = self.evaluate(stmt.value)
                break
            else:
                self.evaluate(stmt)

        # Pop the scope
        self.pop_scope()

        return self.evaluate(result)
    
    def register_stdlib_functions(self):
        import stdlib
        for func_name in dir(stdlib):
            if func_name.startswith("muni_"):
                self.functions[func_name[5:]] = getattr(stdlib, func_name)
    
    def handle_import(self, node):
        module_path = node.module_path
        alias = node.as_name if node.as_name is not None else ""

        if module_path.endswith(':py'):
            module_path = module_path[:-3]
            imported_module = importlib.import_module(module_path)
            self.update_functions_with_alias(imported_module.__dict__, alias)

        elif module_path.endswith('.mun'):
            if not os.path.exists(module_path):
                raise FileNotFoundError(f"File {module_path} not found")

            
            imported_ast = muni_parser.parse_file(module_path)
            # Evaluate the imported AST with a temporary scope for functions
            original_functions = self.functions.copy()
            self.functions = {}
            for statement in imported_ast.statements:
                self.evaluate(statement)

            # Restore original functions and update with imported functions using alias
            imported_functions = self.functions
            self.functions = original_functions
            self.update_functions_with_alias(imported_functions, alias)

    def update_functions_with_alias(self, imported_functions, alias):
        for func_name in imported_functions:
            if alias:
                self.functions[f"{alias}_{func_name}"] = imported_functions[func_name]
            else:
                self.functions[func_name] = imported_functions[func_name]
             
    def perform_cast(self, to_type, value):
        # Example casting logic
        if to_type == 'int':
            if isinstance(value, Muni_Int):
                return value
            elif isinstance(value, Muni_Float):
                return Muni_Int(int(value.value))
            elif isinstance(value, Muni_BasedNumber):
                return Muni_Int(int(value.value))
            elif isinstance(value, Muni_Boolean):
                return Muni_Int(int(value.value))
            
            try:
                return Muni_Int(int(value))
            except ValueError:
                raise Exception(f"Cannot cast {type(value)} to {to_type}")
        
        elif to_type == 'float':
            if isinstance(value, Muni_Int):
                return Muni_Float(value.value)
            elif isinstance(value, Muni_Float):
                return Muni_Float(value.value)
            elif isinstance(value, Muni_BasedNumber):
                return Muni_Float(value.value)
            elif isinstance(value, Muni_Boolean):
                return Muni_Float(value.value)
            try:
                return Muni_Float(float(value))
            except ValueError:
                raise Exception(f"Cannot cast {type(value)} to {to_type}")
        

        elif to_type == 'complex':
            if isinstance(value, Muni_Int):
                return Muni_Complex(value.value, 0)
            elif isinstance(value, Muni_Float):
                return Muni_Complex(value.value, 0)
            elif isinstance(value, Muni_BasedNumber):
                return Muni_Complex(value.value, 0)
            elif isinstance(value, Muni_Complex):
                return value
            elif isinstance(value, Muni_Boolean):
                return Muni_Complex(value.value, 0)
            try:
                return Muni_Complex(value.real, value.imag)
            except:
                raise Exception(f"Cannot cast {type(value)} to {to_type}")
        
        

        elif to_type == 'boolean':
            if isinstance(value, Muni_Int):
                return Muni_Boolean(value.value != 0)
            elif isinstance(value, Muni_Float):
                return Muni_Boolean(value.value != 0)
            elif isinstance(value, Muni_BasedNumber):
                return Muni_Boolean(value.value != 0)
            elif isinstance(value, Muni_Boolean):
                return value
            
            try:
                return Muni_Boolean(bool(value))
            except:
                raise Exception(f"Cannot cast {type(value)} to {to_type}")
        
        elif to_type == 'string':
            if isinstance(value, Muni_Int):
                return Muni_String(str(value.value))
            elif isinstance(value, Muni_Float):
                return Muni_String(str(value.value))
            elif isinstance(value, Muni_BasedNumber):
                return Muni_String(str(value.value))
            elif isinstance(value, Muni_Boolean):
                return Muni_String(str(value.value))
            elif isinstance(value, Muni_String):
                return value
            try:
                return Muni_String(str(value))
            except:
                raise Exception(f"Cannot cast {type(value)} to {to_type}")
        elif 'list' in to_type:
            if '<' in to_type:
                to_type = ('list', to_type[to_type.index('<') + 1:to_type.index('>')])
            if isinstance(value, Muni_List):
                return value
            return Muni_List(value, to_type[1])
        else:
            raise Exception(f"Cannot cast {type(value)} to {to_type}")
    def evaluate_block(self, statements):
        try:
            for statement in statements:
                self.evaluate(statement)
        except:
            self.evaluate(statements) 
    
    