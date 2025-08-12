"""Decorators for FastShell."""

from typing import Callable, Optional, Any
from functools import wraps

from .command import Command


def command(name: Optional[str] = None, description: Optional[str] = None, **kwargs):
    """Decorator to mark a function as a shell command.
    
    This decorator can be used standalone or with a FastShell app instance.
    
    Args:
        name: Command name (defaults to function name)
        description: Command description (overrides docstring)
        **kwargs: Additional command options
        
    Returns:
        Decorated function or decorator
    """
    def decorator(func: Callable) -> Callable:
        # Store command metadata on the function
        cmd_name = name or func.__name__
        cmd_description = description
        
        # Create command instance
        command_obj = Command.from_function(func, cmd_name, **kwargs)
        if cmd_description:
            command_obj.description = cmd_description
        
        # Store command object on function for later retrieval
        func._fastshell_command = command_obj
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper._fastshell_command = command_obj
        return wrapper
    
    return decorator


def argument(description: str = "", **kwargs):
    """Decorator to add metadata to function arguments.
    
    Args:
        description: Argument description
        **kwargs: Additional argument options
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        if not hasattr(func, '_fastshell_arg_metadata'):
            func._fastshell_arg_metadata = {}
        
        # This would need to be applied to specific parameters
        # For now, we'll store the metadata for later use
        func._fastshell_arg_metadata.update(kwargs)
        
        return func
    
    return decorator


def option(description: str = "", **kwargs):
    """Decorator to add metadata to function options.
    
    Args:
        description: Option description
        **kwargs: Additional option metadata
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        if not hasattr(func, '_fastshell_opt_metadata'):
            func._fastshell_opt_metadata = {}
        
        func._fastshell_opt_metadata.update(kwargs)
        
        return func
    
    return decorator