# Muni Language Interpreter

![Muni Logo](images/muni_logo.png)

## Getting Started with Muni

### Introduction
Welcome to Muni, a dynamic, expressive programming language designed for ease of use and readability. This guide will help you set up your development environment and walk you through writing your first Muni script.

### Setting Up Your Development Environment

#### Prerequisites
- A modern operating system (Windows, macOS, or Linux)
- Python 3.6 or later

#### Installation
1. **Download Muni Interpreter:** You can download the latest version of the Muni interpreter from the [GitHub repository](https://github.com/AntoineBlondon/Muni-Interpreter).
2. **Install Dependencies:** Muni requires Python 3.6 or later. Ensure you have Python installed on your system. You can download Python from [python.org](https://www.python.org/downloads/).

#### Setting Up the Interpreter
- Extract the downloaded Muni interpreter to a directory of your choice.
- Add the Muni interpreter's directory to your system's PATH environment variable for easy access from the command line.

See [Installation and Setup](#installation-and-setup) for more details.

### Writing Your First Muni Script

#### Create a New Script
- Open your favorite text editor or IDE.
- Create a new file with the `.mun` extension, for example, `hello_world.mun`.

#### Write a Simple Program
Let's write a simple script that prints "Hello, World!" to the console.

```muni
# hello_world.mun
print("Hello, World!");
```

#### Running Your Script
- Open a terminal or command prompt.
- Navigate to the directory containing your script.
- Run the script with the Muni interpreter:

  ```
  mun hello_world.mun
  ```

You should see "Hello, World!" printed in the console.

### Next Steps
- **Experiment:** Try modifying the `hello_world.mun` script to print different messages.
- **Learn More:** Read the [Muni Language Reference](docs/Language_Reference/Syntax.md) to understand more about Muni's syntax and features.
- **Practice:** Write more scripts to familiarize yourself with Muni's syntax and standard library.

### Getting Help
- **Documentation:** Refer to the [Muni documentation](docs/) for detailed guides and references.
- **Issues:** If you encounter any issues or have suggestions, please report them on the [GitHub issues page](https://github.com/AntoineBlondon/Muni-Interpreter/issues).

Congratulations on running your first Muni script! You're now ready to explore the world of Muni programming. Happy coding!

---

## Muni Language - Syntax Overview


### Introduction

Muni is a dynamically typed, interpreted language. It offers a range of features from basic arithmetic to complex data structures, providing the flexibility needed for modern programming.

### Comments

- Single-line comments start with `#`.
- Multi-line comments are enclosed in `/* ... */`.

```muni
# This is a single-line comment
/*
  This is a multi-line comment
*/
```

### Data Types

Muni supports several data types, including:

- Integers (`int`)
- Floating-point numbers (`float`)
- Complex numbers (`complex`)
- Based numbers (`based`)
- Booleans (`boolean`)
- Strings (`string`)
- Untyped (`?`)

See [Data Types](docs/Language_Reference/Data_Types.md) for more details.

### Variables

Variables in Muni are dynamically typed and declared using the following syntax:

```muni
int myVar = 5;  # Integer
float rate = 3.14;  # Floating-point number
```

### Operators

Muni includes a variety of operators for arithmetic, logical, and comparison operations.

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Logical: `&`, `|`, `!`
- Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`

### Control Structures

Control structures in Muni include `if`, `for`, `while`, `until`, and `switch` statements for managing the flow of the program.

### Functions

Functions are declared with a return type, name, and parameters. They encapsulate reusable code blocks.

```muni
int add(int a, int b) {
    return a + b;
}
```

### Signals

Signals are a unique feature in Muni for event-driven programming. Signals can be emitted and listened to within the program.

```muni
signal mySignal; # Declares a signal 

when (mySignal) {
    # Code to execute when mySignal is emitted (Gets executed in a new thread)
}

emit mySignal;
```

Signals can also be linked to variables mutating using the `watch` keyword.

```muni

int a = 0;

watch (a) {
    # Code to execute when the variable 'a' changes its value
}

a += 1; # the watch statement is executed

```

### Modules

Muni supports modular programming through the use of import statements. Files can be imported to include additional functionality.

```muni
# To import muni files
import <file_name.mun>;

# Example:
import <foo.mun>;

# to import a muni library
import <muni_library:lib>;

# Example:
import <requests:lib>;
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

print(sqrt(25)); # -> 5.0

```

Aliases can be added to differenciate functions

```muni
import <math:py> as m;

float v = m_sqrt(2);
```

### Error Handling (Not implemented yet)

Muni will provide error handling mechanisms such as `try-catch` blocks for robust and error-resistant code.

```muni
try {
    # Code that might throw an error
} catch (ErrorType error) {
    # Error handling code
}
```

This overview provides a glimpse into the syntax and capabilities of the Muni programming language. For more detailed information, please refer to the specific documentation files on various aspects of the language.

---

## Installation and Setup

[This section has not been written yet]

---

## Usage

[This section has not been written yet]

---

## Updating the Interpreter

[This section has not been written yet]

---

## Documentation

The Muni Language Interpreter comes with comprehensive documentation to help you understand and make the most out of Muni. All documentation is located in the [docs](docs/) folder of the repository. Here’s how you can use the documentation to your advantage:

### Accessing Documentation

1. **Online**: The most up-to-date documentation can be accessed directly on GitHub. Visit [https://github.com/AntoineBlondon/Muni-Interpreter/tree/master/docs](https://github.com/AntoineBlondon/Muni-Interpreter/tree/master/docs) to browse through the documentation files.

2. **Offline**: If you've cloned the repository or downloaded the source, you can find the documentation in the [docs](docs/) directory. This is especially useful if you prefer to access documentation offline or if you want to have a local copy for quick reference.

### Key Documentation Files

- `README.md`: An overview of the Muni project, including how to get started.
- `Language_Reference/Syntax.md`: Detailed syntax reference for Muni programming.
- `Standard_Library/Functions.md`: Documentation on the standard library functions available in Muni.
- `Contributing.md`: Guidelines on how to contribute to the Muni project, including code contributions, documentation improvements, and bug reporting.

---

## Contributing to Muni

[This section has not been written yet]

---

## License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details.

---

