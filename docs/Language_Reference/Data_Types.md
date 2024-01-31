# Data Types in Muni Language

## Overview
Muni language offers a variety of data types to cater to different needs in programming. Understanding these data types is crucial for effective programming in Muni. This document outlines each data type, its characteristics, and usage examples.

## Basic Data Types

### Integer (`int`)
- Represents whole numbers.
- Example: `int a = 5;`

### Floating Point (`float`)
- Represents decimal numbers.
- Example: `float b = 3.14;`

### Boolean (`boolean`)
- Represents logical values: `true` or `false`.
- Example: `boolean c = true;`

### String (`string`)
- Represents sequences of characters.
- Example: `string d = "Hello, Muni!";`

### Based Number (`based`)
- Represents numbers in various bases (e.g., binary, hexadecimal) up to base 36 (0-9,A-Z).
- Syntax: `<base>@<value>`.
- Example: `based e = 2@1111;` # binary representation of 15

### Complex Number (`complex`)
- Represents complex numbers with real and imaginary parts.
- Example: `complex f = 3 + 4j;`

### Void (`void`)
- Represents the absence of a value.
- Primarily used in function declarations.

## Advanced Data Types

### Lists (`list`)
- Represents a collection of elements.
- Example: `list<int> g = [1, 2, 3];`

### Dictionaries (`dict`)
- Represents a collection of key-value pairs.
- Example: `dict<string, int> h = {"one": 1, "two": 2};`

### Untyped (`?`)
- Represents a variable whose type is not specified.
- Allows dynamic typing.
Example:
```muni
? var = "A variable";
print(var); # displays the string value "A variable"
var = 3;
print(var); # displays the int value 3
```

## Type Conversion
Muni supports explicit type conversions to ensure proper handling of different data types. 

- **Casting Example**: `int j = int -> 3.14;`
- **Conversion Functions**: `string k = string -> 10;`

## Special Considerations
- **Type Safety**: Muni enforces type safety but allows flexibility with the untyped (`?`) type.
- **Immutability**: By default, Muni treats basic data types as immutable. However, collections like lists and dictionaries can be modified.

## Usage Examples
```mun
int num = 42;
float pi = 3.14159;
boolean isReady = false;
string name = "Muni Language";
based hexNumber = 16@1A;
complex z = 2 + 3j;
? dynamicVar = "This is dynamic";
```
