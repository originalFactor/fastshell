#!/usr/bin/env python3
"""Example FastShell application."""

import os
from typing import Optional, List
from enum import Enum

from fastshell import FastShell


class LogLevel(Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


# Create FastShell app
app = FastShell(name="example-shell", description="An example FastShell application")


@app.command()
def hello(name: str = "World", count: int = 1, uppercase: bool = False):
    """Say hello to someone.
    
    Args:
        name: The name to greet
        count: Number of times to greet
        uppercase: Whether to use uppercase
    """
    greeting = f"Hello, {name}!"
    if uppercase:
        greeting = greeting.upper()
    
    for _ in range(count):
        print(greeting)


@app.command()
def add(a: int, b: int, verbose: bool = False):
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        verbose: Show detailed output
    """
    result = a + b
    if verbose:
        print(f"Adding {a} and {b}...")
        print(f"Result: {result}")
    else:
        print(result)


@app.command()
def list_files(directory: str = ".", pattern: Optional[str] = None, recursive: bool = False):
    """List files in a directory.
    
    Args:
        directory: Directory to list
        pattern: File pattern to match
        recursive: Search recursively
    """
    import glob
    
    if recursive:
        search_pattern = os.path.join(directory, "**", pattern or "*")
        files = glob.glob(search_pattern, recursive=True)
    else:
        search_pattern = os.path.join(directory, pattern or "*")
        files = glob.glob(search_pattern)
    
    for file in sorted(files):
        if os.path.isfile(file):
            size = os.path.getsize(file)
            print(f"{file} ({size} bytes)")
        elif os.path.isdir(file):
            print(f"{file}/ (directory)")


@app.command()
def log(message: str, level: LogLevel = LogLevel.INFO, timestamp: bool = True):
    """Log a message with specified level.
    
    Args:
        message: Message to log
        level: Log level
        timestamp: Include timestamp
    """
    import datetime
    
    prefix = f"[{level.value.upper()}]"
    if timestamp:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prefix = f"[{now}] {prefix}"
    
    print(f"{prefix} {message}")


@app.command()
def calc(expression: str):
    """Evaluate a mathematical expression.
    
    Args:
        expression: Mathematical expression to evaluate
    """
    try:
        # Simple and safe evaluation for basic math
        allowed_chars = set('0123456789+-*/()., ')
        if not all(c in allowed_chars for c in expression):
            print("Error: Only basic mathematical operations are allowed")
            return
        
        result = eval(expression)
        print(f"{expression} = {result}")
    except Exception as e:
        print(f"Error: {e}")


@app.command()
def config(key: Optional[str] = None, value: Optional[str] = None, list_all: bool = False):
    """Manage configuration settings.
    
    Args:
        key: Configuration key
        value: Configuration value (set if provided)
        list_all: List all configuration settings
    """
    # Simple in-memory config for demo
    if not hasattr(config, '_settings'):
        config._settings = {
            'theme': 'dark',
            'auto_save': 'true',
            'max_history': '100'
        }
    
    if list_all:
        print("Configuration settings:")
        for k, v in config._settings.items():
            print(f"  {k} = {v}")
    elif key and value:
        config._settings[key] = value
        print(f"Set {key} = {value}")
    elif key:
        if key in config._settings:
            print(f"{key} = {config._settings[key]}")
        else:
            print(f"Configuration key '{key}' not found")
    else:
        print("Usage: config [--key KEY] [--value VALUE] [--list-all]")


@app.command()
def search(query: str, files: List[str], case_sensitive: bool = False, line_numbers: bool = False):
    """Search for text in files.
    
    Args:
        query: Text to search for
        files: List of files to search in (comma-separated)
        case_sensitive: Perform case-sensitive search
        line_numbers: Show line numbers
    """
    import re
    
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = re.compile(query, flags)
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if pattern.search(line):
                        line = line.rstrip('\n')
                        if line_numbers:
                            print(f"{file_path}:{line_num}: {line}")
                        else:
                            print(f"{file_path}: {line}")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")


if __name__ == "__main__":
    app.run()