# RIO 🌊

> A simple programming language that transpiles to Python — learn it at the speed of a river.

**RIO** (Spanish for "river") is a small programming language designed to be **fast to learn and easy to read**, built as a transpiler on top of Python. Every RIO program compiles to 100% valid Python and runs directly.

```
cls Greeter:
    new(name):
        me.name = name
    fanc hello():
        return "Hello {me.name}!"

g = Greeter("World")
prn g.hello()
```

---

## ✨ Why RIO?

| | |
|---|---|
| 🪶 **Lightweight** | A complete transpiler in a single file, under 20 KB, zero external dependencies |
| ⚡ **Fast to learn** | Simple syntax (`prn`, `set`, `rep`, `fanc`) — hours if you already know a language, days if you're a total beginner |
| 🧩 **Concise** | Shorter than Python, Ruby, JavaScript, Java, and C++ for the same program (see the comparison below) |
| 🐍 **Fully Python-compatible** | Import any Python library (numpy, requests, scikit-learn...) and use it directly |
| 🛡️ **Built-in error checker** | Validates function and class argument counts before running |

---

## 🚀 Installation & Usage

Requires only Python 3.6+ (no extra installation needed):

```bash
python3 rio.py myprogram.rio --run
```

The `.f` extension is also accepted instead of `.rio`.

---

## 📖 Quick Syntax Guide

### Printing & Variables
```
prn "Hello"          # print with a newline
prt "no newline"      # print without a newline
x = 5                  # variable (set is optional)
prn "The value: {x}"   # automatic string interpolation, no need for f-strings
```

### Conditionals & Loops
```
if x > 10:
    prn "big"
elif x > 0:
    prn "small positive"
else:
    prn "negative or zero"

rep i in 1..5:          # counting loop
    prn i

rep item in [1,2,3]:     # loop over any collection
    prn item

while x > 0:
    x = x - 1
```

### Functions
```
fanc square(n) = n * n           # single-line function

fanc factorial(n):                # multi-line function body
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

### Classes
```
cls Point:
    new(x, y):
        me.x = x
        me.y = y
    fanc distance_from_origin():
        return (me.x ** 2 + me.y ** 2) ** 0.5
```

### Error Handling
```
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

### Imports
```
import requests                            # any Python library
from sklearn.linear_model import LinearRegression
use "helpers.rio"                           # another RIO file
```

---

## 📊 Comparison (same program, every language)

A program that sums the squares of even numbers from 1 to 10:

| Language | Actual character count |
|---|---|
| **RIO** | **78** |
| Ruby | 117 |
| Python | 127 |
| JavaScript | 166 |
| PHP | 174 |
| Java | 245 |
| C++ | 248 |

---

## ⚠️ Known Limitations (full transparency)

- The word `me` is fully reserved inside any class (it maps to `self`)
- `use "file.rio"` imports **everything** from the file — no selective imports yet
- The error checker only validates argument counts, not types or logic
- Relatively slow at runtime (runs through the Python interpreter) — not suited for high-performance applications

---

## 📄 License

Add your preferred license here (MIT is suggested for small open-source projects).
