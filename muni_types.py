from math import sqrt
class Muni_Type:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Muni_Int(Muni_Type):
    def __init__(self, value):
        if not isinstance(value, int):
            raise TypeError("Muni_Int requires an integer value")
        super().__init__(value)

    def __add__(self, other):
        if isinstance(other, Muni_Int):
            return Muni_Int(self.value + other.value)
        elif isinstance(other, Muni_Float):
            return Muni_Float(self.value + other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(str(self.value + other.value), other.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value + other.real, other.imag)
        elif isinstance(other, Muni_String):
            return Muni_String(str(self) + other.value)
        
        raise TypeError("Unsupported operand type(s) for +: 'Muni_Int' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, Muni_Int):
            return Muni_Int(self.value - other.value)
        elif isinstance(other, Muni_Float):
            return Muni_Float(self.value - other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(str(self.value - other.value), other.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value - other.real, -other.imag)
        
        raise TypeError("Unsupported operand type(s) for -: 'Muni_Int' and '{}'".format(type(other).__name__))

    def __mul__(self, other):
        if isinstance(other, Muni_Int):
            return Muni_Int(self.value * other.value)
        elif isinstance(other, Muni_Float):
            return Muni_Float(self.value * other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(str(self.value * other.value), other.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value * other.real, self.value * other.imag)
        
        raise TypeError("Unsupported operand type(s) for *: 'Muni_Int' and '{}'".format(type(other).__name__))

    def __truediv__(self, other):
        if isinstance(other, Muni_Int):
            if other.value == 0:
                raise ValueError("Error: Division by zero")
            return Muni_Float(self.value / other.value)  # Integer division
        elif isinstance(other, Muni_Float):
            return Muni_Float(self.value / other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(str(self.value / other.value), other.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex((self.value*other.real) / (other.modulus())**2, (self.value*other.imag) / (other.modulus())**2)
        
        raise TypeError("Unsupported operand type(s) for /: 'Muni_Int' and '{}'".format(type(other).__name__))

    # Floor Division
    def __floordiv__(self, other):
        if isinstance(other, Muni_Int):
            if other.value == 0:
                raise ValueError("Error: Division by zero")
            return Muni_Int(self.value // other.value)
        elif isinstance(other, Muni_Float):
            return Muni_Int(self.value // other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(str(self.value // other.value), other.base)
        raise TypeError("Unsupported operand type for //: 'Muni_Int' and '{}'".format(type(other).__name__))

    # Modulus
    def __mod__(self, other):
        if isinstance(other, Muni_Int):
            if other.value == 0:
                raise ValueError("Modulus by zero")
            return Muni_Int(self.value % other.value)
        elif isinstance(other, Muni_Float):
            return Muni_Float(self.value % other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(str(self.value % other.value), other.base)
        raise TypeError("Unsupported operand type for %: 'Muni_Int' and '{}'".format(type(other).__name__))

    # Comparison operations
    def __eq__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value == other.value)
        
        return Muni_Boolean(False)

    def __ne__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value != other.value)
        return Muni_Boolean(True)

    def __lt__(self, other):
        if isinstance(other, (Muni_Int, Muni_Float, Muni_BasedNumber)):
            return Muni_Boolean(self.value < other.value)
        raise TypeError("Unsupported operand type for <: 'Muni_Int' and '{}'".format(type(other).__name__))

    def __le__(self, other):
        if isinstance(other, (Muni_Int, Muni_Float, Muni_BasedNumber)):
            return Muni_Boolean(self.value <= other.value)
        raise TypeError("Unsupported operand type for <=: 'Muni_Int' and '{}'".format(type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, (Muni_Int, Muni_Float, Muni_BasedNumber)):
            return Muni_Boolean(self.value > other.value)
        raise TypeError("Unsupported operand type for >: 'Muni_Int' and '{}'".format(type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, (Muni_Int, Muni_Float, Muni_BasedNumber)):
            return Muni_Boolean(self.value >= other.value)
        raise TypeError("Unsupported operand type for >=: 'Muni_Int' and '{}'".format(type(other).__name__))

    # Type Conversion Methods
    def to_muni_float(self):
        return Muni_Float(float(self.value))
    
    def to_muni_based(self, new_base):
        return Muni_BasedNumber(str(self.value), new_base)
    
    def to_muni_complex(self):
        return Muni_Complex(self.value, 0)

    def to_muni_string(self):
        return Muni_String(str(self.value))

    def __str__(self):
        return str(self.value)
    
    def __int__(self):
        return int(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __hash__(self):
        return hash(self.value)
    
    def symbol():
        return 'int'


class Muni_BasedNumber(Muni_Type):
    def __init__(self, value, base):
        if base < 2 or base > 36:
            raise ValueError("Base must be between 2 and 36")
        self.base = base
        self.value = self._convert_to_decimal(value, base)

    def _convert_to_decimal(self, value, base):
        try:
            return int(str(value), base)
        except ValueError:
            raise ValueError(f"Invalid value {value} for base {base}")
        
    def to_base(self, new_base):
        if new_base < 2 or new_base > 36:
            raise ValueError("Base must be between 2 and 36")
        return Muni_BasedNumber(self.str_to_base(new_base), new_base)

    def str_to_base(self, new_base):
        if new_base < 2 or new_base > 36:
            raise ValueError("Base must be between 2 and 36")
        return self._convert_from_decimal(self.value, new_base)

    def _convert_from_decimal(self, number, base):
        if number == 0:
            return '0'
        digits = []
        while number:
            digits.append(int_to_base_digit(number % base))
            number //= base
        return ''.join(reversed(digits))
    
    def __add__(self, other):
        if isinstance(other, Muni_Float):
            return Muni_Float(self.value + other.value)
        elif isinstance(other, Muni_Int):
            return Muni_BasedNumber(self.value + other.value, self.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value + other.real, other.imag)
        elif isinstance(other, Muni_String):
            return Muni_String(str(self) + other.value)
        raise TypeError("Unsupported operand type(s) for +: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def add(self, other, base):
        if isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(self.value + other.value, base)
        raise TypeError("Unsupported operand type(s) for +: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def __sub__(self, other):
        if isinstance(other, Muni_Float):
            return Muni_Float(self.value - other.value)
        elif isinstance(other, Muni_Int):
            return Muni_BasedNumber(self.value - other.value, self.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value - other.real, -other.imag)
        raise TypeError("Unsupported operand type(s) for -: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def subtract(self, other, base):
        if isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(self.value - other.value, base)
        raise TypeError("Unsupported operand type(s) for -: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def __mul__(self, other):
        if isinstance(other, Muni_Float):
            return Muni_Float(self.value * other.value)
        elif isinstance(other, Muni_Int):
            return Muni_BasedNumber(self.value * other.value, self.base)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value * other.real, self.value * other.imag)
        raise TypeError("Unsupported operand type(s) for *: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def multiply(self, other, base):
        if isinstance(other, Muni_BasedNumber):
            return Muni_BasedNumber(self.value * other.value, base)
        raise TypeError("Unsupported operand type(s) for *: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def __truediv__(self, other):
        if isinstance(other, Muni_Float):
            return Muni_Float(self.value / other.value)
        elif isinstance(other, Muni_Int):
            return Muni_Float(self.value / other.value)
        elif isinstance(other, Muni_Complex):
            return Muni_Complex((self.value*other.real) / (other.modulus())**2, (self.value*other.imag) / (other.modulus())**2)
        raise TypeError("Unsupported operand type(s) for /: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def divide(self, other):
        if isinstance(other, Muni_BasedNumber):
            return Muni_Float(self.value / other.value)
        raise TypeError("Unsupported operand type(s) for /: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    
    def __mod__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber, Muni_Float)):
            return Muni_Int(self.value % other.value)
        raise TypeError("Unsupported operand type(s) for %: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))

    def __str__(self):
        return f"{self.base}@{self.str_to_base(self.base)}"
    
    def __int__(self):
        return self.value
    
    def __float__(self):
        return float(self.value)
    
    def __hash__(self):
        return hash(self.value)
    
    
    def symbol():
        return 'based'

    # Add other methods for arithmetic, comparisons, etc.
    # Comparisons 
    def __eq__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value == other.value)
        raise TypeError("Unsupported operand type for ==: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    def __ne__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value != other.value)
        raise TypeError("Unsupported operand type for !=: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    def __lt__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber, Muni_Float)):
            return Muni_Boolean(self.value < other.value)
        raise TypeError("Unsupported operand type for <: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    def __le__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber, Muni_Float)):
            return Muni_Boolean(self.value <= other.value)
        raise TypeError("Unsupported operand type for <=: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    def __gt__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber, Muni_Float)):
            return Muni_Boolean(self.value > other.value)
        raise TypeError("Unsupported operand type for >: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    def __ge__(self, other):
        if isinstance(other, (Muni_Int, Muni_BasedNumber, Muni_Float)):
            return Muni_Boolean(self.value >= other.value)
        raise TypeError("Unsupported operand type for >=: 'Muni_BasedNumber' and '{}'".format(type(other).__name__))
    

class Muni_Complex(Muni_Type):
    def __init__(self, real, imag):

        self.real = float(real)
        self.imag = float(imag)

    def __add__(self, other):
        if isinstance(other, Muni_Complex):
            return Muni_Complex(self.real + other.real, self.imag + other.imag)
        elif isinstance(other, Muni_String):
            return Muni_String(str(self) + other.value)
        raise TypeError("Unsupported operand type(s) for +: 'Muni_Complex' and '{}'".format(type(other).__name__))
    def modulus(self):
        return Muni_Float(sqrt(self.real**2 + self.imag**2))
    
    def __str__(self):
        return f"{self.real} + {self.imag}j"
    
    def __complex__(self):
        return complex(self.real, self.imag)

    def symbol():
        return 'complex'

class Muni_Float(Muni_Type):
    def __init__(self, value):
        if not isinstance(value, float):
            try:  # Try converting to float
                value = float(value)
            except ValueError:
                raise TypeError("Muni_Float requires a float value")
        super().__init__(float(value))

    def __add__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int)):
            return Muni_Float(self.value + other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_Float(str(self.value + other.value))
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value + other.real, other.imag)
        elif isinstance(other, Muni_String):
            return Muni_String(str(self.value) + other.value)
        raise TypeError("Unsupported operand type(s) for +: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __sub__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int)):
            return Muni_Float(self.value - other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_Float(str(self.value - other.value))
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value - other.real, -other.imag)
        raise TypeError("Unsupported operand type(s) for -: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __mul__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int)):
            return Muni_Float(self.value * other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_Float(str(self.value * other.value))
        elif isinstance(other, Muni_Complex):
            return Muni_Complex(self.value * other.real, self.value * other.imag)
        raise TypeError("Unsupported operand type(s) for *: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __truediv__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int)):
            if other.value == 0:
                raise ValueError("Error: Division by zero")
            return Muni_Float(self.value / other.value)
        elif isinstance(other, Muni_BasedNumber):
            return Muni_Float(str(self.value / other.value))
        elif isinstance(other, Muni_Complex):
            return Muni_Complex((self.value*other.real) / (other.modulus())**2, (self.value*other.imag) / (other.modulus())**2)
        raise TypeError("Unsupported operand type(s) for /: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __floordiv__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int, Muni_BasedNumber)):
            if other.value == 0:
                raise ValueError("Error: Division by zero")
            return Muni_Float(self.value // other.value)
        raise TypeError("Unsupported operand type for //: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __mod__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int, Muni_BasedNumber)):
            if other.value == 0:
                raise ValueError("Modulus by zero")
            return Muni_Float(self.value % other.value)
        raise TypeError("Unsupported operand type for %: 'Muni_Float' and '{}'".format(type(other).__name__))

    # Comparison operations
    def __eq__(self, other):
        if isinstance(other, Muni_Float):
            return Muni_Boolean(self.value == other.value)
        return Muni_Boolean(False)

    def __ne__(self, other):
        if isinstance(other, Muni_Float):
            return Muni_Boolean(self.value != other.value)
        return Muni_Boolean(True)

    def __lt__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value < other.value)
        raise TypeError("Unsupported operand type for <: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __le__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value <= other.value)
        raise TypeError("Unsupported operand type for <=: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __gt__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value > other.value)
        raise TypeError("Unsupported operand type for >: 'Muni_Float' and '{}'".format(type(other).__name__))

    def __ge__(self, other):
        if isinstance(other, (Muni_Float, Muni_Int, Muni_BasedNumber)):
            return Muni_Boolean(self.value >= other.value)
        raise TypeError("Unsupported operand type for >=: 'Muni_Float' and '{}'".format(type(other).__name__))

    def to_muni_string(self):
        return Muni_String(str(self.value))

    def __str__(self):
        return str(self.value)
    
    def __float__(self):
        return float(self.value)
    
    def __hash__(self):
        return hash(self.value)
    

    def symbol():
        return 'float'





class Muni_Boolean(Muni_Type):
    def __init__(self, value):
        if not isinstance(value, bool):
            try:  # Try converting to float
                value = bool(value)
            except ValueError:
                raise TypeError("Muni_Boolean requires a boolean value")
        super().__init__(bool(value))
    def __eq__(self, other):
        if isinstance(other, Muni_Boolean):
            return Muni_Boolean(self.value == other.value)
        raise TypeError("Unsupported operand type(s) for ==: 'Muni_Boolean' and '{}'".format(type(other).__name__))
    
    def __ne__(self, other):
        if isinstance(other, Muni_Boolean):
            return Muni_Boolean(self.value != other.value)
        raise TypeError("Unsupported operand type(s) for !=: 'Muni_Boolean' and '{}'".format(type(other).__name__))
    
    def __not__(self):
        return Muni_Boolean(not self.value)

    def __and__(self, other):
        if isinstance(other, Muni_Boolean):
            return Muni_Boolean(self.value and other.value)
        raise TypeError("Unsupported operand type(s) for &: 'Muni_Boolean' and '{}'".format(type(other).__name__))

    def __or__(self, other):
        if isinstance(other, Muni_Boolean):
            return Muni_Boolean(self.value or other.value)
        raise TypeError("Unsupported operand type(s) for |: 'Muni_Boolean' and '{}'".format(type(other).__name__))
    
    def __xor__(self, other):
        if isinstance(other, Muni_Boolean):
            return Muni_Boolean(self.value ^ other.value)
        raise TypeError("Unsupported operand type(s) for ^: 'Muni_Boolean' and '{}'".format(type(other).__name__))

    def __add__(self, other):
        if isinstance(other, Muni_String):
            return Muni_String(str(self.value) + other.value)
        raise TypeError("Unsupported operand type(s) for +: 'Muni_Boolean' and '{}'".format(type(other).__name__))

    def __str__(self):
        return "true" if self.value else "false"
    
    def __bool__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    
    def symbol():
        return 'boolean'
    


class Muni_String(Muni_Type):
    def __init__(self, value):
        if not isinstance(value, str):
            raise TypeError("Muni_String requires a string value")
        super().__init__(value)
    
    def __add__(self, other):
        if isinstance(other, Muni_String):
            return Muni_String(self.value + other.value)
        elif isinstance(other, (Muni_Int, Muni_Float, Muni_BasedNumber, Muni_Boolean)):
            return Muni_String(self.value + str(other))
        raise TypeError("Unsupported operand type(s) for +: 'Muni_String' and '{}'".format(type(other).__name__))
    # Add more methods specific to string operations

    def __str__(self):
        return self.value
    
    def __hash__(self):
        return hash(self.value)
    
    
    def __iter__(self):
        return iter(self.value)
    
    def symbol():
        return 'string'

class Muni_Void(Muni_Type):
    def __init__(self):
        super().__init__(None)

    def __str__(self):
        return "void"
    
    def symbol():
        return 'void'

class Muni_Untyped(Muni_Type):
    def __init__(self):
        super().__init__(None)

    def symbol():
        return '?'

class Muni_List(Muni_Type):
    def __init__(self, items=None, type_specifier='UNTYPED'):
        super().__init__(items if items is not None else [])
        self.type_specifier = type_specifier
        for item in items:
            self.check_type(item)

    def append(self, item):
        self.check_type(item)    
        self.value.append(item)
        
    
    def remove(self, item):
        self.value.remove(item)

    def get_item(self, index):
        return self.value[index]
    
    def set_item(self, index, item):
        self.check_type(item)
        self.value[index] = item
    
    def insert(self, index, item):
        self.check_type(item)
        self.value.insert(index, item)

    
    
    
    
    def check_type(self, item):
        if self.type_specifier != "UNTYPED" and not isinstance(item, types[self.type_specifier]):
            raise TypeError(f"Expected type {types[self.type_specifier]}, got {type(item)}")
            
    

    def __iter__(self):
        return iter(self.value)
    
    def __str__(self):
        try:
            return f"<{types[self.type_specifier].symbol()}>[{', '.join(str(item) for item in self.value)}]"
        except KeyError as e:
            return f"<{self.type_specifier}>[{', '.join(str(item) for item in self.value)}]"

    # Add more list-specific methods like remove, get, etc.
    def symbol(self):
        return f'list<{self.type_specifier}>'

class Muni_Dict(Muni_Type):
    def __init__(self, dict_values=None):
        super().__init__(dict_values if dict_values is not None else {})

    def set_item(self, key, item):
        if not isinstance(item, Muni_Type):
            raise TypeError("Values must be Muni_Type instances")
        self.value[key] = item

    def get_item(self, key):
        return self.value.get(key, Muni_Void())


# You can add more methods and functionalities as needed
    

def int_to_base_digit(digit):
    if digit < 10:
        return str(digit)
    return chr(ord('a') + digit - 10)



types = {
    "UNTYPED": Muni_Untyped,
    "INT": Muni_Int,
    "FLOAT": Muni_Float,
    "BASED": Muni_BasedNumber,
    "COMPLEX": Muni_Complex,
    "BOOLEAN": Muni_Boolean,
    "STRING": Muni_String,
    "VOID": Muni_Void,
    "LIST": Muni_List,
    "DICT": Muni_Dict,
    "int": Muni_Int,
    "float": Muni_Float,
    "boolean": Muni_Boolean,
    "based": Muni_BasedNumber,
    "complex": Muni_Complex,
    "string": Muni_String,
    "void": Muni_Void,
    "list": Muni_List,
    "dict": Muni_Dict,
    "?": Muni_Untyped


}