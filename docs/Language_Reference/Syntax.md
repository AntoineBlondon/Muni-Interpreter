# Muni Language - Syntax Overview

Welcome to the Muni Language Syntax Overview. This document provides a high-level overview of the syntax used in the Muni programming language, designed for clarity and expressiveness. Muni supports a variety of features, making it a versatile choice for various programming tasks.

## Table of Contents

1. [Introduction](#introduction)
2. [Comments](#comments)
3. [Data Types](#data-types)
4. [Variables](#variables)
5. [Operators](#operators)
6. [Control Structures](#control-structures)
7. [Functions](#functions)
8. [Signals](#signals)
9. [Modules](#modules)
10. [Error Handling](#error-handling)

## Introduction

Muni is a dynamically typed, interpreted language. It offers a range of features from basic arithmetic to complex data structures, providing the flexibility needed for modern programming.

## Comments

- Single-line comments start with `#`.
- Multi-line comments are enclosed in `/* ... */`.

```muni
# This is a single-line comment
/*
  This is a multi-line comment
*/
```

## Data Types

Muni supports several data types, including:

- Integers (`int`)
- Floating-point numbers (`float`)
- Complex numbers (`complex`)
- Booleans (`boolean`)
- Strings (`string`)
- Untyped (`?`)

## Variables

Variables in Muni are dynamically typed and declared using the following syntax:

```muni
int myVar = 5;  # Integer
float rate = 3.14;  # Floating-point number
```

## Operators

Muni includes a variety of operators for arithmetic, logical, and comparison operations.

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Logical: `&`, `|`, `!`
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`

## Control Structures

Control structures in Muni include `if`, `for`, `while`, `until`, and `switch` statements for managing the flow of the program.

## Functions

Functions are declared with a return type, name, and parameters. They encapsulate reusable code blocks.

```muni
int add(int a, int b) {
    return a + b;
}
```

## Signals

Signals are a unique feature in Muni for event-driven programming. Signals can be emitted and listened to within the program.

```muni
signal mySignal; # Declares a signal 

when (mySignal) {
    # Code to execute when mySignal is emitted
}


emit mySignal;
```

## Modules

Muni supports modular programming through the use of import statements. Files can be imported to include additional functionality.

```muni
import <file_name>;
```

Python files and modules can be imported as well:
```python
# hello.py
def say_hello():
    print("hi")
```

```muni
# my_script.mun
import <hello:py> # imports the local hello.py file
import <math:py> # imports the python math module

say_hello(); # Displays "hi"

print(sqrt(25)) # -> 5.0

```


## Error Handling (Not implemented yet)

Muni will provide error handling mechanisms such as `try-catch` blocks for robust and error-resistant code.

```muni
try {
    # Code that might throw an error
} catch (ErrorType error) {
    # Error handling code
}
```

This overview provides a glimpse into the syntax and capabilities of the Muni programming language. For more detailed information, please refer to the specific documentation files on various aspects of the language.