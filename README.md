# FastShell

A FastAPI-like framework for building interactive shell applications with automatic completion, type conversion, and subcommands.

## Features

- 🚀 **FastAPI-like decorators** - Simple and intuitive API design
- 📝 **Automatic parsing** - Docstrings, function names, parameters, and type annotations
- 🔧 **Auto-completion** - Command and parameter completion with TUI support
- 🌳 **Subcommands** - Nested command structure support
- 🔄 **Type conversion** - Automatic parameter type conversion
- 🖥️ **Cross-platform** - Works on Windows, macOS, and Linux
- 🎨 **Rich output** - Beautiful terminal output with colors and formatting

## Quick Start

```python
from fastshell import FastShell

app = FastShell()

@app.command()
def hello(name: str = "World"):
    """Say hello to someone.
    
    Args:
        name: The name to greet
    """
    print(f"Hello, {name}!")

@app.command()
def add(a: int, b: int):
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
    """
    result = a + b
    print(f"{a} + {b} = {result}")

if __name__ == "__main__":
    app.run()
```

## Installation

```bash
pip install fastshell-framework
```

## Development Installation

For development, clone the repository and install in editable mode:

```bash
git clone https://github.com/fastshell/fastshell.git
cd fastshell
pip install -e .
```

## Development

```bash
pip install -e ".[dev]"
```

## License

MIT License