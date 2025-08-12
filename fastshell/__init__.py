"""FastShell - A FastAPI-like framework for building interactive shell applications."""

from .app import FastShell
from .decorators import command
from .types import Argument, Option

__version__ = "0.1.0"
__all__ = ["FastShell", "command", "Argument", "Option"]