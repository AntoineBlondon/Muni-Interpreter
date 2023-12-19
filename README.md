# Muni Language Interpreter

## Introduction

Muni is a modern, statically & dynamically typed programming language designed for simplicity and efficiency. This repository contains the Muni Language Interpreter, an implementation of the Muni language written in Python. Muni supports various data types, control flow statements, functions, and unique features like signal-based programming.

## Features

- **Static & Dynamic Typing:** Muni supports various data types like integers, floats, strings, booleans, complex numbers, and more.
- **Control Flow Constructs:** Includes `if/else`, `for`, `while`, `until`, and `switch` statements.
- **Functions:** Define and call functions with ease.
- **Signal Programming:** A unique feature that allows asynchronous programming using signals.
- **Error Handling:** Robust error handling with try-catch blocks. (Not implemented yet)
- **Modules:** Import custom modules to extend functionality.

## Installation

Clone the repository:

```bash
git clone https://github.com/AntoineBlondon/Muni-Interpreter.git
cd Muni-Interpreter/scripts
chmod +x mun
mv mun /usr/local/bin/
```

## Usage

To run a Muni script:

```bash
mun your_script.mun
```

## Updating

To update the interpreter:

```bash
mun --update
```

## Documentation

For detailed documentation on the Muni language syntax and features, refer to the [Docs](docs/) directory in this repository.

## Contributing

Contributions to the Muni language interpreter are welcome. Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details.
