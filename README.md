# RIO 🌊

A compact, easy-to-learn programming language that transpiles to Python. RIO (Spanish for "river") focuses on readability and speed of learning — it compiles to valid Python so you can use any Python library.

---

## Overview

RIO is a small transpiled language designed for clarity and fast onboarding. The entire transpiler is intentionally lightweight and aims to let you write concise code that runs on the Python ecosystem.

Key principles:
- Readability: Simple, expressive syntax.
- Learnability: Minimal keywords and straightforward constructs.
- Interoperability: Output is 100% valid Python so you can import Python packages directly.

---

## Features

- Single-file, zero-dependency transpiler (small footprint)
- Direct interoperability with Python libraries (numpy, requests, scikit-learn, etc.)
- Built-in argument-count validation before execution
- Concise syntax for functions, classes, loops, and conditionals

---

## Quick Example

RIO code:

```rio
cls Greeter:
    new(name):
        me.name = name
    fanc hello():
        return "Hello {me.name}!"

g = Greeter("World")
prn g.hello()
```

This compiles to Python and runs on the Python interpreter.

---

## Installation

Requires Python 3.6+.

Run a RIO file:

```bash
python3 rio.py myprogram.rio --run
```

RIO files may also use the `.f` extension.

---

## Quick Syntax Guide

Printing & variables

```rio
prn "Hello"            # print with newline
prt "no newline"       # print without newline
x = 5                   # variable assignment (set keyword optional)
prn "The value: {x}"    # automatic string interpolation
```

Conditionals & loops

```rio
if x > 10:
    prn "big"
elif x > 0:
    prn "small positive"
else:
    prn "negative or zero"

rep i in 1..5:          # counting loop
    prn i

rep item in [1,2,3]:    # iterate over collections
    prn item

while x > 0:
    x = x - 1
```

Functions

```rio
fanc square(n) = n * n   # single-line function

fanc factorial(n):        # multi-line function
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Classes

```rio
cls Point:
    new(x, y):
        me.x = x
        me.y = y
    fanc distance_from_origin():
        return (me.x ** 2 + me.y ** 2) ** 0.5
```

Error handling

```rio
try:
    result = 10 / 0
catch e:
    prn "An error occurred: {e}"
finally:
    prn "Done"

fanc check(n):
    if n < 0:
        fail "Number must be positive"
    return n
```

Imports

```rio
import requests
from sklearn.linear_model import LinearRegression
use "helpers.rio"   # import another RIO file
```

---

## Comparison (conciseness)

Example: sum squares of even numbers from 1 to 10 (character count):

| Language | Characters |
|---|---:|
| RIO | 78 |
| Ruby | 117 |
| Python | 127 |
| JavaScript | 166 |
| PHP | 174 |
| Java | 245 |
| C++ | 248 |

---

## Known Limitations

- `me` is reserved inside classes (maps to Python `self`).
- `use "file.rio"` imports everything from the target file; selective imports are not supported yet.
- The built-in checker validates argument counts only (no static type checking).
- Runtime performance depends on the Python interpreter; RIO is not optimized for high-performance workloads.

---

## Contributing

Contributions are welcome. Suggested next steps for contributors:

1. Fork the repository and create a feature branch.
2. Add tests for any new features or bug fixes.
3. Open a pull request with a clear description of the change.

Consider adding GitHub Actions for automated linting and testing.

---

## License

This project does not yet include a license. For open-source sharing, consider the MIT license.

---

If you'd like, I can also:
- Add a CONTRIBUTING.md and CODE_OF_CONDUCT.md
- Add GitHub Actions workflows for CI (tests/lint)
- Create issue and PR templates

Tell me which of these to add next or if you want me to commit the README update directly (I have prepared it).