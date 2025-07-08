# rpipe

R-like pipe functionality for Python using the `>>` operator.

## Installation

```bash
pip install git+https://github.com/priscian/rpipe.git
# Or to force reinstallation:
pip install --force-reinstall --no-cache-dir git+https://github.com/priscian/rpipe.git
```

Or install from source:

```bash
git clone https://github.com/priscian/rpipe.git
cd rpipe
pip install -e .
```

## Quick Start

```python
from rpipe import P, pipe, TF, TL, partial

# Basic usage with P and >>
result = range(5) >> P(list)
# [0, 1, 2, 3, 4]

# Traditional pipe function
result = pipe(range(5), list, sum)
# 10

# Thread-first (TF)
result = TF(10, (lambda x, y: x / y, 2), str)
# '5.0'

# Thread-last (TL)
result = TL(2, (pow, 3))
# 8

# Combining with partial
add_10 = partial(lambda x, y: x + y, 10)
result = 5 >> P(add_10)
# 15
```

## Features

- **R-like piping**: Use the `>>` operator for intuitive data pipelines
- **Flexible syntax**: Works with single values, tuples, and function chains
- **Integration with toolz**: Built on top of the powerful `toolz.pipe` function
- **Partial function support**: Seamlessly works with `functools.partial`

## Examples

### Basic Piping

```python
from rpipe import P

# Simple transformation
[1, 2, 3, 4, 5] >> P(sum)  # 15

# Multiple transformations
range(10) >> P(
    list,
    lambda x: [i**2 for i in x],
    sum
)  # 285
```

### Using with functools.partial

```python
from rpipe import P
from functools import partial

# Create reusable functions
add_10 = partial(lambda x, y: x + y, 10)
multiply_by = lambda factor: partial(lambda x, y: x * y, factor)

result = 5 >> P(
    add_10,           # 5 + 10 = 15
    multiply_by(2)()  # 15 * 2 = 30
)  # 30
```

### Complex Data Processing

```python
from rpipe import P
from functools import partial

# Data processing pipeline
data = ["apple", "banana", "cherry", "date"]

result = data >> P(
    partial(filter, lambda x: len(x) > 5),
    list,
    partial(map, str.upper),
    list,
    sorted,
    lambda x: ", ".join(x)
)
# "BANANA, CHERRY"
```

## API Reference

### `P`

The main pipe object that enables the `>>` operator syntax.

- `P(func1, func2, ...)` - Creates a pipeline of functions
- `P(data, func1, func2, ...)` - Immediately executes the pipeline with data
- `data >> P(func1, func2, ...)` - Pipes data through a series of functions

### `pipe`

The original `toolz.pipe` function for traditional functional piping.

```python
pipe(data, func1, func2, func3)  # Passes data through func1, then func2, then func3
```

### `TF` (thread_first)

Thread-first macro from toolz - threads the value as the first argument.

```python
TF(x, (f, a, b), (g, c))  # Equivalent to g(f(x, a, b), c)
```

### `TL` (thread_last)

Thread-last macro from toolz - threads the value as the last argument.

```python
TL(x, (f, a, b), (g, c))  # Equivalent to g(c, f(a, b, x))
```

### `partial`

From functools - creates partial functions by fixing some arguments.

```python
add = lambda x, y: x + y
add_10 = partial(add, 10)  # Creates a function that adds 10
```

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=rpipe
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Jim Java - james.j.java@gmail.com

## Acknowledgments

- Built on top of the excellent [toolz](https://github.com/pytoolz/toolz) library
- Inspired by R's pipe operator and magrittr's `%>%`
