#!/usr/bin/env python3
"""
Enhanced type validation using Pydantic for FastShell.

This module provides advanced type validation capabilities using Pydantic,
including support for complex types, custom validators, and better error messages.
"""

import types
from typing import Any, Type, Union, get_origin, get_args
from pydantic import BaseModel, ValidationError, Field

from .exceptions import TypeConversionError


class ValidationConfig:
    """Configuration for validation behavior."""
    
    def __init__(self, use_pydantic: bool = True, strict_mode: bool = False):
        self.use_pydantic = use_pydantic
        self.strict_mode = strict_mode


class EnhancedValidator:
    """Enhanced type validator using Pydantic."""
    
    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
    
    def validate_and_convert(self, value: str, target_type: Type, field_name: str = "value") -> Any:
        """Validate and convert a string value to the target type using Pydantic.
        
        Args:
            value: String value to convert
            target_type: Target type to convert to
            field_name: Name of the field for error reporting
            
        Returns:
            Converted value
            
        Raises:
            TypeConversionError: If conversion fails
        """
        if not self.config.use_pydantic:
            # Fallback to original validation
            return self._fallback_convert(value, target_type)
        
        try:
            # Create a dynamic Pydantic model for validation
            model_fields = {
                field_name: (target_type, Field(...))
            }
            
            # Configure model with strict validation
            class Config:
                str_strip_whitespace = True
                validate_assignment = True
                # Allow coercion for basic types but be strict about invalid values
                
            DynamicModel = type(
                'DynamicValidationModel',
                (BaseModel,),
                {
                    '__annotations__': {field_name: target_type},
                    'Config': Config,
                    **model_fields
                }
            )
            
            # Create model instance with the value
            model_data = {field_name: value}
            instance = DynamicModel(**model_data)
            
            return getattr(instance, field_name)
            
        except ValidationError as e:
            # Extract meaningful error message
            error_msg = self._format_pydantic_error(e, field_name, target_type)
            raise TypeConversionError(error_msg)
        except Exception as e:
            # Fallback for any other errors
            return self._fallback_convert(value, target_type)
    
    def _format_pydantic_error(self, error: ValidationError, field_name: str, target_type: Type) -> str:
        """Format Pydantic validation error into a user-friendly message."""
        errors = error.errors()
        if not errors:
            return f"Cannot convert to {self._format_type_name(target_type)}"
        
        first_error = errors[0]
        error_type = first_error.get('type', 'validation_error')
        error_msg = first_error.get('msg', 'Invalid value')
        
        # Customize error messages for common cases
        if error_type == 'int_parsing':
            return f"Cannot convert to integer: {error_msg}"
        elif error_type == 'float_parsing':
            return f"Cannot convert to float: {error_msg}"
        elif error_type == 'bool_parsing':
            return f"Cannot convert to boolean: {error_msg}"
        elif 'union' in error_type:
            return f"Cannot convert to {self._format_type_name(target_type)}: {error_msg}"
        else:
            return f"Cannot convert to {self._format_type_name(target_type)}: {error_msg}"
    
    def _fallback_convert(self, value: str, target_type: Type) -> Any:
        """Fallback conversion method (original logic)."""
        from .utils import convert_value
        return convert_value(value, target_type)
    
    def _format_type_name(self, type_obj: Type) -> str:
        """Format a type object into a readable string."""
        if isinstance(type_obj, types.UnionType):
            # Handle new-style Union types (Python 3.10+)
            args = type_obj.__args__
            if len(args) == 2 and type(None) in args:
                non_none_type = args[0] if args[1] == type(None) else args[1]
                return f"Optional[{self._format_type_name(non_none_type)}]"
            else:
                arg_names = [self._format_type_name(arg) for arg in args]
                return f"Union[{', '.join(arg_names)}]"
        elif hasattr(type_obj, '__name__'):
            return type_obj.__name__
        elif hasattr(type_obj, '__origin__'):
            origin = get_origin(type_obj)
            if origin == Union:
                args = get_args(type_obj)
                if len(args) == 2 and type(None) in args:
                    non_none_type = args[0] if args[1] == type(None) else args[1]
                    return f"Optional[{self._format_type_name(non_none_type)}]"
                else:
                    arg_names = [self._format_type_name(arg) for arg in args]
                    return f"Union[{', '.join(arg_names)}]"
            elif origin in (list, List):
                args = get_args(type_obj)
                if args:
                    item_type = self._format_type_name(args[0])
                    return f"List[{item_type}]"
                else:
                    return "List"
            else:
                return str(type_obj)
        else:
            return str(type_obj)


# Global validator instance
_global_validator = EnhancedValidator()


def set_validation_config(config: ValidationConfig):
    """Set global validation configuration."""
    global _global_validator
    _global_validator = EnhancedValidator(config)


def validate_and_convert(value: str, target_type: Type, field_name: str = "value") -> Any:
    """Global function for type validation and conversion."""
    return _global_validator.validate_and_convert(value, target_type, field_name)


# Import List for type annotations
try:
    from typing import List
except ImportError:
    List = list