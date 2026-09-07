# RIO Programming Language

> A simple, readable programming language that compiles to Python.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status: Experimental](https://img.shields.io/badge/status-experimental-orange.svg)](https://github.com/abidinfan8-wq/Rio-n-programming-language)
[![Version](https://img.shields.io/badge/version-5.1-blue.svg)](https://github.com/abidinfan8-wq/Rio-n-programming-language/releases)

## What is RIO?

RIO is a programming language with concise, clear syntax. The compiler converts RIO programs into executable Python code, allowing you to use Python libraries while retaining RIO syntax.

The project is currently experimental. RIO 6 is under development and will include a Lexer, Parser, AST, standard library, and package manager.

## Quick Example

```rio
fanc greet(name):
    return "Hello {name}!"

prn greet("RIO")

rep i in 1..3:
    prn i
```

## Features

- Variables and arithmetic operations.
- `if`, `elif`, and `else` conditionals.
- `rep` and `while` loops.
- Functions using `fanc`.
- Classes and constructors using `cls` and `new`.
- Error handling using `try`, `catch`, and `finally`.
- Automatic string interpolation using `{expression}`.
- The ability to use Python libraries.
- Beginner-friendly error messages.

## Requirements

- Python 3.6 or later for RIO 5.
- No external dependencies are required for the core version.

## Usage

```bash
python3 rio-5.py examples/hello.rio --run
```

## Project Status

| Version | Status |
|---|---|
| RIO 5.1 | Usable experimental release |
| RIO 6 | Under development |

## RIO 6 Roadmap

- Full Lexer.
- Parser and AST.
- Semantic analyzer.
- Error messages linked to the original RIO file.
- A dedicated RIO standard library.
- Package manager.
- Automated tests and expanded documentation.

## Contributing

Suggestions, examples, documentation, and pull requests are welcome. Please read the [contribution guide](CONTRIBUTING.md) before submitting changes.

## Security

Do not run untrusted RIO files; they can use Python functions and imported libraries. See the [security policy](SECURITY.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Links

- [Syntax Guide](docs/SYNTAX.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [GitHub Repository](https://github.com/abidinfan8-wq/Rio-n-programming-language)
