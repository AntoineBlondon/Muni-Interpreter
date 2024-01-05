from muni_types import *


class AstNode:
    def __init__(self, lineno=None, col_offset=None):
        self.lineno = lineno
        self.col_offset = col_offset

class StatementList(AstNode):
    def __init__(self, statements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.statements = statements
    
    def __str__(self):
        return "\n".join([str(statement) for statement in self.statements])

    def __repr__(self):
        return self.__str__()

class BinaryOperation(AstNode):
    def __init__(self, left, operator, right, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"BinaryOperation({self.left}, '{self.operator}', {self.right})"

    def __repr__(self):
        return self.__str__()

class LogicalOperation(AstNode):
    def __init__(self, left, operator, right, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"LogicalOperation({self.left}, '{self.operator}', {self.right})"

    def __repr__(self):
        return self.__str__()

class ComparisonOperation(AstNode):
    def __init__(self, left, operator, right, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self):
        return f"ComparisonOperation({self.left}, '{self.operator}', {self.right})"

    def __repr__(self):
        return self.__str__()

class NotOperation(AstNode):
    def __init__(self, operand, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.operand = operand

    def __str__(self):
        return f"NotOperation({self.operand})"
    
    def __repr__(self):
        return self.__str__()

class UnaryOperation(AstNode):
    def __init__(self, operand, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.operand = operand

    def __str__(self):
        return f"UnaryOperation({self.operand})"

    def __repr__(self):
        return self.__str__()


class Number(AstNode):
    def __init__(self, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        if not isinstance(value, (Muni_Int, Muni_Float, Muni_Complex, Muni_BasedNumber)):
            raise TypeError("Number node requires a Muni number type")
        self.value = value

    def __str__(self):
        return f"Number({self.value})"

    def __repr__(self):
        return self.__str__()

class Boolean(AstNode):
    def __init__(self, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        if not isinstance(value, Muni_Boolean):
            raise TypeError("Boolean node requires a Muni_Boolean type")
        self.value = value
    
    def __str__(self):
        return f"Boolean({self.value})"

    def __repr__(self):
        return self.__str__()

class String(AstNode):
    def __init__(self, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        if not isinstance(value, Muni_String):
            raise TypeError("String node requires a Muni_String type")
        self.value = value

    def __str__(self):
        return f"String({self.value})"

    def __repr__(self):
        return self.__str__()



class Assignment(AstNode):
    def __init__(self, name, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.name = name
        self.value = value

    def __str__(self):
        return f"Assignment(name='{self.name}', value={self.value})"

class ExpressionAssignment(AstNode):
    def __init__(self, name, operator, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.name = name
        self.operator = operator
        self.value = value

    def __str__(self):
        return f"ExpressionAssignment(name='{self.name}', operator='{self.operator}', value={self.value})"

class Declaration(AstNode):
    def __init__(self, type_specifier, name, value=None, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.type_specifier = type_specifier
        self.name = name
        self.value = value

    def __str__(self):
        return f"Declaration(type='{self.type_specifier}', name='{self.name}', value={self.value})"


class ListInitialization(AstNode):
    def __init__(self, elements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.elements = elements
    
    def __str__(self):
        return f"ListInitialization({self.elements})"

class DictInitialization(AstNode):
    def __init__(self, elements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.elements = elements

    def __str__(self):
        return f"DictInitialization({self.elements})"

class ElementAccess(AstNode):
    def __init__(self, expression, index, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.expression = expression 
        self.index = index

    def __str__(self):
        return f"ElementAccess(expression='{self.expression}', index={self.index})"
    

class ElementAssignment(AstNode):
    def __init__(self, name, index, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.name = name
        self.index = index
        self.value = value

    def __str__(self):
        return f"ElementAssignment(name='{self.name}', index={self.index}, value={self.value})"

class Variable(AstNode):
    def __init__(self, name, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.name = name

    def __str__(self):
        return f"Variable(name='{self.name}')"


class FunctionCall(AstNode):
    def __init__(self, name, arguments, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.name = name
        self.arguments = arguments

    def __str__(self):
        args = ", ".join(map(str, self.arguments))
        return f"FunctionCall(name={self.name}, args=[{args}])"



class FunctionDeclaration(AstNode):
    def __init__(self, name, return_type, parameters, body, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.name = name
        self.return_type = return_type
        self.parameters = parameters
        self.body = body

    def __str__(self):
        params = ", ".join([f"{ptype} {pname}" for ptype, pname in self.parameters])
        return f"FunctionDeclaration(name={self.name}, return_type={self.return_type}, params=[{params}], body=[{', '.join([str(x) for x in self.body])}])"


class Return(AstNode):
    def __init__(self, value, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.value = value


class ImportStatement(AstNode):
    def __init__(self, module_path, as_name=None, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.module_path = module_path
        self.as_name = as_name


class Cast(AstNode):
    def __init__(self, to_type, expression, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.to_type = to_type
        self.expression = expression

    def __str__(self):
        return f"Cast(to_type='{self.to_type}', expression={self.expression})"


class IfStatement(AstNode):
    def __init__(self, condition, true_block, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.condition = condition
        self.true_block = true_block
    
    def __str__(self):
        return f"IfStatement(condition={self.condition}, true_block={self.true_block})"


class IfElseStatement(AstNode):
    def __init__(self, condition, true_block, false_block, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def __str__(self):
        return f"IfElseStatement(condition={self.condition}, true_block={self.true_block}, false_block={self.false_block})"


class WhileStatement(AstNode):
    def __init__(self, condition, body, nb_iterations=0, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.condition = condition
        self.body = body
        self.nb_iterations = nb_iterations

    def __str__(self):
        return f"WhileStatement(condition={self.condition}, body={','.join([str(statement) for statement in self.body])}, nb_iterations={self.nb_iterations})"


class UntilStatement(AstNode):
    def __init__(self, condition, body, nb_iterations=0, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.condition = condition
        self.body = body
        self.nb_iterations = nb_iterations

    def __str__(self):
        return f"UntilStatement(condition={self.condition}, body={','.join([str(statement) for statement in self.body])}, nb_iterations={self.nb_iterations})"


class ForInStatement(AstNode):
    def __init__(self, type_specifier, identifier, iterable, body, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.type_specifier = type_specifier
        self.identifier = identifier
        self.iterable = iterable
        self.body = body
    
    def __str__(self):
        return f"ForInStatement(type_specifier={self.type_specifier}, identifier={self.identifier}, iterable={self.iterable}, body={','.join([str(statement) for statement in self.body])})"


class ForStatement(AstNode):
    def __init__(self, begin_statement, condition, end_statement, body, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.begin_statement = begin_statement
        self.condition = condition
        self.end_statement = end_statement
        self.body = body

    def __str__(self):
        return f"ForStatement(begin_statement={self.begin_statement}, condition={self.condition}, end_statement={self.end_statement}, body={','.join([str(statement) for statement in self.body])})"
    


class SwitchStatement(AstNode):
    def __init__(self, expression, cases, default_case, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.expression = expression
        self.cases = cases
        self.default_case = default_case
    
    def __str__(self):
        return f"SwitchStatement(expression={self.expression}, cases={self.cases}, default_case={self.default_case})"

class CaseClause(AstNode):
    def __init__(self, value, statements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.value = value
        self.statements = statements

    def __str__(self):
        return f"CaseClause(value={self.value}, statements={','.join([str(statement) for statement in self.statements])})"

class DefaultClause(AstNode):
    def __init__(self, statements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.statements = statements

    def __str__(self):
        return f"DefaultClause(statements={','.join([str(statement) for statement in self.statements])})"


class SignalDeclaration(AstNode):
    def __init__(self, signal_name, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.signal_name = signal_name
    
    def __str__(self):
        return f"SignalDeclaration(signal_name={self.signal_name})"

class EmitStatement(AstNode):
    def __init__(self, signal_name, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.signal_name = signal_name
    
    def __str__(self):
        return f"EmitStatement(signal_name={self.signal_name})"
    


class WatchStatement(AstNode):
    def __init__(self, variable_name, statements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.variable_name = variable_name
        self.statements = statements
    
    def __str__(self):
        return f"WatchStatement(variable_name={self.variable_name}, statements={','.join([str(statement) for statement in self.statements])})"
class WhenStatement(AstNode):
    def __init__(self, signal_name, statements, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.signal_name = signal_name
        self.statements = statements
    
    def __str__(self):
        return f"WhenStatement(signal_name={self.signal_name}, statements={','.join([str(statement) for statement in self.statements])})"


class Range(AstNode):
    def __init__(self, start, end, step, inclusive=False, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.start = start
        self.end = end
        self.step = step
        self.inclusive = inclusive
    
    def __str__(self):
        return f"Range(start={self.start}, end={self.end}, step={self.step}, inclusive={self.inclusive})"


class ThrowStatement(AstNode):
    def __init__(self, expression, lineno=None, col_offset=None):
        super().__init__(lineno, col_offset)
        self.expression = expression
    
    def __str__(self):
        return f"ThrowStatement(expression={self.expression})"