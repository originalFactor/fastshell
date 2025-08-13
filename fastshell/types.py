"""Type definitions for FastShell."""

from enum import Enum
from typing import Any, Type, Optional
from dataclasses import dataclass


class ParameterType(Enum):
    """Parameter type enumeration."""
    ARGUMENT = "argument"  # Positional argument
    OPTION = "option"     # Named option/flag


@dataclass
class Parameter:
    """Represents a command parameter."""
    
    name: str
    type: Type
    description: str = ""
    default: Any = None
    required: bool = True
    parameter_type: ParameterType = ParameterType.ARGUMENT
    
    @property
    def is_flag(self) -> bool:
        """Check if parameter is a boolean flag."""
        return self.type == bool and self.parameter_type == ParameterType.OPTION


@dataclass
class ParsedCommand:
    """Represents a parsed command line."""
    
    command: Optional[str] = None
    args: list = None
    kwargs: dict = None
    
    def __post_init__(self):
        if self.args is None:
            self.args = []
        if self.kwargs is None:
            self.kwargs = {}
