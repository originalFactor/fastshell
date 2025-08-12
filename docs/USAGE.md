# FastShell Usage Guide

## Quick Start

### 1. Basic Application

```python
from fastshell import FastShell

app = FastShell(name="my-shell", description="My custom shell")

@app.command()
def greet(name: str, times: int = 1):
    """Greet someone.
    
    Args:
        name: Person to greet
        times: Number of greetings
    """
    for _ in range(times):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    app.run()
```

### 2. Running the Application

**Interactive Mode:**
```bash
python my_app.py
```

**Command Line Mode:**
```bash
python my_app.py greet Alice --times 3
```

## Features

### 1. Automatic Type Conversion

FastShell automatically converts command line arguments to the correct Python types based on type annotations:

```python
@app.command()
def calculate(a: int, b: float, operation: str = "add"):
    """Perform calculations.
    
    Args:
        a: First number (integer)
        b: Second number (float)
        operation: Operation to perform
    """
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
```

Usage:
```bash
my-shell> calculate 10 3.14 --operation multiply
```

### 2. Boolean Flags

```python
@app.command()
def process_file(filename: str, verbose: bool = False, backup: bool = True):
    """Process a file.
    
    Args:
        filename: File to process
        verbose: Enable verbose output
        backup: Create backup before processing
    """
    if backup:
        print(f"Creating backup of {filename}")
    
    if verbose:
        print(f"Processing {filename} with verbose output")
    else:
        print(f"Processing {filename}")
```

Usage:
```bash
my-shell> process_file data.txt --verbose --no-backup
```

### 3. Enum Support

```python
from enum import Enum

class LogLevel(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"

@app.command()
def log_message(message: str, level: LogLevel = LogLevel.INFO):
    """Log a message.
    
    Args:
        message: Message to log
        level: Log level
    """
    print(f"[{level.value.upper()}] {message}")
```

Usage:
```bash
my-shell> log_message "Something happened" --level warning
```

### 4. List Parameters

```python
from typing import List

@app.command()
def process_files(files: List[str], pattern: str = "*.txt"):
    """Process multiple files.
    
    Args:
        files: List of files to process (comma-separated)
        pattern: File pattern to match
    """
    for file in files:
        print(f"Processing {file} with pattern {pattern}")
```

Usage:
```bash
my-shell> process_files file1.txt,file2.txt,file3.txt --pattern "*.log"
```

### 5. Optional Parameters

```python
from typing import Optional

@app.command()
def search(query: str, directory: Optional[str] = None, recursive: bool = False):
    """Search for files.
    
    Args:
        query: Search query
        directory: Directory to search in (defaults to current)
        recursive: Search recursively
    """
    search_dir = directory or "."
    print(f"Searching for '{query}' in {search_dir}")
    if recursive:
        print("Searching recursively")
```

### 6. Auto-completion

FastShell provides intelligent auto-completion for:

- **Command names**: Tab completion for available commands
- **Parameter names**: Auto-complete `--parameter-name`
- **Parameter values**: Type-aware value suggestions
- **Enum values**: Auto-complete enum member names
- **Boolean values**: Suggests `true`/`false`

### 7. Help System

**General help:**
```bash
my-shell> help
```

**Command-specific help:**
```bash
my-shell> command_name --help
```

### 8. Rich Output

FastShell uses the Rich library for beautiful terminal output with colors and formatting.

## Advanced Usage

### Custom Command Classes

```python
from fastshell import FastShell
from fastshell.command import Command
from fastshell.types import Parameter, ParameterType

app = FastShell()

# Create custom command
def custom_func(name: str):
    print(f"Custom: {name}")

custom_command = Command.from_function(custom_func, "custom")
app.add_command(custom_command)
```

### Error Handling

```python
from fastshell.exceptions import FastShellException, InvalidArguments

@app.command()
def risky_operation(value: int):
    """Perform a risky operation.
    
    Args:
        value: Input value
    """
    if value < 0:
        raise InvalidArguments("Value must be positive")
    
    if value > 100:
        raise FastShellException("Value too large")
    
    print(f"Processing value: {value}")
```

### Subcommands (Future Enhancement)

```python
# This is a planned feature for future versions
from fastshell import FastShell, Group

app = FastShell()
db_group = Group(name="db")

@db_group.command()
def migrate():
    """Run database migrations."""
    print("Running migrations...")

@db_group.command()
def seed():
    """Seed the database."""
    print("Seeding database...")

app.add_group(db_group)
```

## Best Practices

1. **Use descriptive docstrings**: They become help text
2. **Provide type annotations**: Enables automatic type conversion
3. **Use meaningful parameter names**: They become command line options
4. **Set sensible defaults**: Makes commands easier to use
5. **Handle errors gracefully**: Use FastShell exceptions for user-friendly error messages
6. **Keep commands focused**: Each command should do one thing well

## Comparison with Other Tools

| Feature | FastShell | Click | argparse | Fire |
|---------|-----------|-------|----------|------|
| Decorator-based | ✅ | ✅ | ❌ | ✅ |
| Auto-completion | ✅ | ✅ | ❌ | ❌ |
| Interactive mode | ✅ | ❌ | ❌ | ❌ |
| Type conversion | ✅ | ✅ | ✅ | ✅ |
| Rich output | ✅ | ❌ | ❌ | ❌ |
| Cross-platform | ✅ | ✅ | ✅ | ✅ |
| Learning curve | Low | Medium | High | Low |

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
2. **Type conversion errors**: Check your type annotations
3. **Command not found**: Verify command registration with `@app.command()`
4. **Auto-completion not working**: Ensure you're in interactive mode

### Debug Mode

```python
app = FastShell(name="my-app", debug=True)  # Enable debug output
```

## Examples

See `example.py` for a comprehensive example application demonstrating all features.