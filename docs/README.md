# FastShell

A FastAPI-like framework for building interactive shell applications with automatic completion, type conversion, and subcommands.

## Features

- 🚀 **FastAPI-like decorators** - Simple and intuitive API design
- 📝 **Automatic parsing** - Docstrings, function names, parameters, and type annotations
- 🔧 **Auto-completion** - Command and parameter completion with TUI support
- 🌳 **Subcommands** - Nested command structure support
- 🔄 **Enhanced type conversion** - Pydantic-powered type validation and conversion
- 🆕 **Modern Union syntax** - Full support for Python 3.10+ `int | str` syntax
- 🛡️ **Robust validation** - Better error messages and type safety
- 🖥️ **Cross-platform** - Works on Windows, macOS, and Linux
- 🎨 **Rich output** - Beautiful terminal output with colors and formatting

## Quick Start

```python
from typing import Union, Optional
from fastshell import FastShell

# Enable Pydantic validation (default)
app = FastShell(use_pydantic=True)

@app.command()
def hello(name: str = "World", count: int = 1):
    """Say hello to someone.
    
    Args:
        name: The name to greet
        count: Number of times to greet
    """
    for _ in range(count):
        print(f"Hello, {name}!")

@app.command()
def process(value: int | str, convert_to: Optional[str] = None):
    """Process a value with modern Union syntax.
    
    Args:
        value: Can be integer or string (Python 3.10+ syntax)
        convert_to: Optional conversion target
    """
    print(f"Processing: {value} (type: {type(value).__name__})")
    return value

@app.command()
def add(a: int, b: int, verbose: bool = False):
    """Add two numbers with optional verbose output.
    
    Args:
        a: First number
        b: Second number
        verbose: Show detailed output
    """
    result = a + b
    if verbose:
        print(f"Adding {a} and {b}...")
    print(f"{a} + {b} = {result}")

if __name__ == "__main__":
    app.run()
```

## Installation

```bash
pip install fastshell
```

## What's New in v2.0

### 🆕 Pydantic Integration

FastShell now includes **Pydantic-powered type validation** for enhanced type safety and better error handling:

- ✅ **Fixed Python 3.10+ Union syntax**: No more `'types.UnionType' object has no attribute '__name__'` errors
- ✅ **Enhanced validation**: More accurate type conversion with better error messages
- ✅ **Backward compatible**: Existing code works without changes
- ✅ **Configurable**: Choose between Pydantic and legacy validation

### Modern Type Syntax Support

```python
# ✅ Now fully supported!
@app.command()
def modern_syntax(value: int | str, optional: str | None = None):
    """Uses Python 3.10+ Union syntax"""
    pass

# ✅ Traditional syntax still works
@app.command()
def traditional_syntax(value: Union[int, str], optional: Optional[str] = None):
    """Uses typing module syntax"""
    pass
```

### Configuration Options

```python
# Enable Pydantic validation (default)
app = FastShell(use_pydantic=True)

# Use legacy validation for performance
app = FastShell(use_pydantic=False)
```

### Enhanced Error Messages

```bash
# Before: Type conversion error: invalid literal for int()
# After: Cannot convert to integer: invalid literal for int() with base 10: 'abc'
```

## Documentation

For detailed information about Pydantic integration, see [PYDANTIC_INTEGRATION.md](PYDANTIC_INTEGRATION.md).

## Development Installation

For development, clone the repository and install in editable mode:

```bash
git clone https://github.com/originalFactor/fastshell.git
cd fastshell
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
```

## Testing

Run the comprehensive test suite:

```bash
python test_comprehensive_validation.py
```
