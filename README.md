# Muni Programming Language

Muni is a custom programming language designed to provide a simple yet powerful ( syntax for various programming tasks. This repository contains the source code for the Muni interpreter, which includes the lexer, parser, and runtime environment.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Custom lexer and parser
- Dynamic typing
- Control flow structures (`if`, `else`, `for`, `while`, etc.)
- Native functions for file I/O, string manipulation, and more
- Modular architecture allowing for easy extensions

## Installation

> Note: An installer will be added later to avoid a mess when installing.

To manually install the Muni interpreter, clone the repository and navigate to its directory:

```bash
git clone https://github.com/AntoineBlondon/Muni-Interpreter.git
cd Mun-Interpreter
```

Then, run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run a Muni script, use the following command:

```bash
python main.py your_script.mun
```

### Example Muni Script

```mun
string greeting = "Hello, world!";
print(greeting);
```
