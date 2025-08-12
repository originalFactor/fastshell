"""Exception classes for FastShell."""


class FastShellException(Exception):
    """Base exception for FastShell."""
    pass


class CommandNotFound(FastShellException):
    """Raised when a command is not found."""
    pass


class InvalidArguments(FastShellException):
    """Raised when command arguments are invalid."""
    pass


class ParseError(FastShellException):
    """Raised when command line parsing fails."""
    pass


class TypeConversionError(FastShellException):
    """Raised when type conversion fails."""
    pass