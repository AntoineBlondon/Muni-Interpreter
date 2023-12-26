from muni_types import *
from muni_ast_nodes import *
from muni_error import *
import importlib
import os
import sys
import muni_parser 
import threading
from muni_context_manager import ContextManager


class Runtime:
    def __init__(self):
        self.scopes = [{}]
        self.functions = {}
        self.signals = {}
        self.watched = {}
        self.is_running = True
        self.lineno = 0
        self.register_stdlib_functions()
        self.context = ContextManager()

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
        
        if(self.is_watched(name)):
                self.execute_watch(name)

    def get_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Muni_Error(f"Variable '{name}' not found")

    def get_scope(self, name):
        for i, scope in enumerate(reversed(self.scopes)):
            if name in scope:
                return len(self.scopes) - i - 1
        raise Muni_Error(f"Variable '{name}' not found")
    
    def is_variable(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False
    
    def define_signal(self, signal_name):
        if signal_name in self.signals:
            raise Muni_Error(f"Signal Error: {signal_name} already a signal.")
        self.signals[signal_name] = None

    def assign_signal(self, signal_name, statements):
        if signal_name not in self.signals:
            raise Muni_Error(f"Signal Error: {signal_name} not a signal.")

        if self.signals[signal_name] is None:
            self.signals[signal_name] = [statements]
        else:
            self.signals[signal_name].append(statements)

    def emit_signal(self, signal_name):
        if signal_name not in self.signals:
            raise Muni_Error(f"Signal Error: {signal_name} not a signal.")
        
        for statements in self.signals[signal_name]:
            thread = threading.Thread(target=self.evaluate_block, args=(statements,))
            thread.start()

    def assign_watching(self, var_name, body):
        if not self.is_variable(var_name):
            raise Muni_Error(f"Variable Error: {var_name} not a variable.")
        
        if not self.is_watched(var_name):
            self.watched[var_name] = []

        self.watched[var_name].append({"scope": self.get_scope(var_name), "body": body})

    def is_watched(self, var_name):
        if not self.is_variable(var_name):
            raise Muni_Error(f"Variable Error: {var_name} not a variable.")
        return var_name in self.watched
    
    def execute_watch(self, var_name):
        if not self.is_variable(var_name):
            raise Muni_Error(f"Variable Error: {var_name} not a variable.")
        
        if not self.is_watched(var_name):
            return
        
        for d_statements in self.watched[var_name]:
            if d_statements["scope"] != self.get_scope(var_name):
                continue
            statements = d_statements["body"]
            thread = threading.Thread(target=self.evaluate_block, args=(statements,))
            thread.start()


    
    def evaluate(self, node, debug=False):
        if debug: print(node)
        if not self.is_running:
            return
        try:
            self.context.set_lineno(node.lineno)
        except:
            pass
        try:
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
                
                if(self.is_watched(node.name)):
                    self.execute_watch(node.name)

            elif isinstance(node, ExpressionAssignment): # a += 1, a -= 1, a /=1 ...
                value = self.evaluate(node.value)
                variable = self.get_variable(node.name)
                try:
                    symbol = type(variable).symbol()
                except Exception as e:
                    symbol = variable.symbol()

                self.define_variable(node.name, self.apply_binary_operator(variable, value, node.operator[:-1]), str(symbol))

                


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
                    if self.is_running == False: return
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
            
            elif isinstance(node, WatchStatement):
                self.assign_watching(node.variable_name, node.statements)

            elif isinstance(node, ListInitialization):
                values = [self.evaluate(val) for val in node.elements]
                return Muni_List(values)
            
            elif isinstance(node, DictInitialization):
                elements = {self.evaluate(key): self.evaluate(value) for key, value in node.elements.items()}
                return Muni_Dict(elements)

            elif isinstance(node, ElementAccess):
                obj = self.evaluate(node.expression)
                index = self.evaluate(node.index)
                return obj.get_item(index)
        
            elif isinstance(node, ElementAccess):
                obj = self.evaluate(node.name)
                index = self.evaluate(node.index)
                value = self.evaluate(node.value)
                obj.set_item(index, value)
                self.define_variable(node.name, obj, str(obj.symbol()))

            elif isinstance(node, Range):
                start = self.evaluate(node.start)
                end = self.evaluate(node.end)
                step = self.evaluate(node.step)
                return Muni_List([Muni_Int(x) for x in list(range(int(start), int(end) + node.inclusive * (-1)**(int(step)<=0), int(step)))], "INT")

            elif isinstance(node, ThrowStatement):
                raise Muni_Error(self.evaluate(node.expression))

            elif self.is_variable(node):
                return self.get_variable(node)

            elif isinstance(node, str):
                return Muni_String(node)
            elif isinstance(node, int):
                return Muni_Int(node)
            elif isinstance(node, float):
                return Muni_Float(node)
            elif isinstance(node, bool):
                return Muni_Boolean(node)
            elif isinstance(node, list):
                return Muni_List(node)  
            
            elif node is None:
                return None
            else:
                raise Muni_Error(f"Unknown node type: {type(node)}")
        except Muni_Error as error:
            print(error)
            self.is_running = False 

    def apply_binary_operator(self, left, right, operator):
        
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            if (right == 0):
                raise Muni_Error("Division by zero")
            
            return left / right
        elif operator == '%':
            return left % right
        else:
            raise Muni_Error(f"Unknown binary operator: {operator}")
        
    def apply_logical_operator(self, left, right, operator):
        if operator == '&':
            return left and right
        elif operator == '|':
            return left or right
        elif operator == '^':
            return left ^ right
        else:
            raise Muni_Error(f"Unknown logical operator: {operator}")
    
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
            raise Muni_Error(f"Unknown comparison operator: {operator}")
        
    def check_type(self, type_specifier, value):
        if type_specifier == 'int':
            if not isinstance(value, Muni_Int):
                raise Muni_Error(f"Expected an int, got {type(value)}")
        elif type_specifier == 'float':
            if not isinstance(value, Muni_Float):
                raise Muni_Error(f"Expected a float, got {type(value)}")
        elif type_specifier == 'complex':
            if not isinstance(value, Muni_Complex):
                raise Muni_Error(f"Expected a complex number, got {type(value)}")
        elif type_specifier == 'boolean':
            if not isinstance(value, Muni_Boolean):
                raise Muni_Error(f"Expected a boolean, got {type(value)}")

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
                raise Muni_Error(f"File {module_path} not found")

            
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
        elif module_path.endswith(':lib'):
            library_name = module_path[:-4]
            library_path = os.path.join(os.path.dirname(__file__), "libraries", f"lib_{library_name}.py")
            if not os.path.exists(library_path):
                raise Muni_Error(f"Library {library_name} not found")
            imported_module = self.import_from_absolute_path(library_path)
            self.update_functions_with_alias(imported_module.__dict__, alias)
            
    def import_from_absolute_path(self, path_to_file):
    # Extract module name and directory path
        module_name = os.path.basename(path_to_file).replace('.py', '')
        directory = os.path.dirname(path_to_file)

        # Add directory to sys.path
        if directory not in sys.path:
            sys.path.append(directory)

        # Load the module
        spec = importlib.util.spec_from_file_location(module_name, path_to_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module
        


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
            elif isinstance(value, type(None)):
                return Muni_Int(0)
            
            try:
                return Muni_Int(int(value))
            except ValueError:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        
        elif to_type == 'float':
            if isinstance(value, Muni_Int):
                return Muni_Float(value.value)
            elif isinstance(value, Muni_Float):
                return Muni_Float(value.value)
            elif isinstance(value, Muni_BasedNumber):
                return Muni_Float(value.value)
            elif isinstance(value, Muni_Boolean):
                return Muni_Float(value.value)
            elif isinstance(value, type(None)):
                return Muni_Float(0)
            try:
                return Muni_Float(float(value))
            except ValueError:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        

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
            elif isinstance(value, type(None)):
                return Muni_Complex(0, 0)
            try:
                return Muni_Complex(value.real, value.imag)
            except:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        
        

        elif to_type == 'boolean':
            if isinstance(value, Muni_Int):
                return Muni_Boolean(value.value != 0)
            elif isinstance(value, Muni_Float):
                return Muni_Boolean(value.value != 0)
            elif isinstance(value, Muni_BasedNumber):
                return Muni_Boolean(value.value != 0)
            elif isinstance(value, Muni_Boolean):
                return value
            elif isinstance(value, type(None)):
                return Muni_Boolean(False)
            
            try:
                return Muni_Boolean(bool(value))
            except:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        
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
            elif isinstance(value, type(None)):
                return Muni_String("")
            try:
                return Muni_String(str(value))
            except:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        elif 'list' in to_type:
            if '<' in to_type:
                to_type = ('list', to_type[to_type.index('<') + 1:to_type.index('>')])
            if isinstance(value, Muni_List):
                return Muni_List(value.value, to_type[1])
            elif isinstance(value, type(None)):
                return Muni_List([])
            try:
                return Muni_List(value, to_type[1])
            except:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        
        elif 'dict' in to_type:
            if isinstance(value, Muni_Dict):
                return Muni_Dict(value.value, to_type[1], to_type[2])
            elif isinstance(value, type(None)):
                return Muni_Dict({})
            try:
                return Muni_Dict(value)
            except:
                raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
        else:
            raise Muni_Error(f"Cannot cast {type(value)} to {to_type}")
    def evaluate_block(self, statements):
        try:
            for statement in statements:
                self.evaluate(statement)
        except:
            self.evaluate(statements) 
    
    