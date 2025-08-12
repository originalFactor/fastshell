"""Utility functions for FastShell."""

import re
from typing import Any, Type, Dict, Union

from .exceptions import TypeConversionError


def parse_docstring(docstring: str) -> Dict[str, Any]:
    """Parse a function docstring to extract description and parameter info.
    
    Args:
        docstring: Function docstring
        
    Returns:
        Dictionary with 'description' and 'parameters' keys
    """
    if not docstring:
        return {"description": "", "parameters": {}}
    
    lines = docstring.strip().split('\n')
    description_lines = []
    parameters = {}
    
    in_args_section = False
    current_param = None
    current_param_desc = []
    
    for line in lines:
        line = line.strip()
        
        if line.lower().startswith('args:') or line.lower().startswith('arguments:'):
            in_args_section = True
            continue
        elif line.lower().startswith(('returns:', 'return:', 'yields:', 'yield:', 'raises:', 'raise:', 'examples:', 'example:', 'note:', 'notes:')):
            # Save current parameter if any
            if current_param and current_param_desc:
                parameters[current_param] = ' '.join(current_param_desc).strip()
            in_args_section = False
            break
        
        if in_args_section:
            # Check if this line starts a new parameter
            param_match = re.match(r'^(\w+)\s*(?:\([^)]+\))?\s*:?\s*(.*)', line)
            if param_match:
                # Save previous parameter
                if current_param and current_param_desc:
                    parameters[current_param] = ' '.join(current_param_desc).strip()
                
                # Start new parameter
                current_param = param_match.group(1)
                current_param_desc = [param_match.group(2)] if param_match.group(2) else []
            elif current_param and line:
                # Continue description of current parameter
                current_param_desc.append(line)
        else:
            # Part of main description
            if line:
                description_lines.append(line)
    
    # Save last parameter
    if current_param and current_param_desc:
        parameters[current_param] = ' '.join(current_param_desc).strip()
    
    description = ' '.join(description_lines).strip()
    
    return {
        "description": description,
        "parameters": parameters
    }


def convert_value(value: str, target_type: Type) -> Any:
    """Convert a string value to the target type.
    
    Args:
        value: String value to convert
        target_type: Target type to convert to
        
    Returns:
        Converted value
        
    Raises:
        TypeConversionError: If conversion fails
    """
    if target_type == str:
        return value
    
    try:
        if target_type == bool:
            return value.lower() in ('true', '1', 'yes', 'on', 'y')
        elif target_type == int:
            return int(value)
        elif target_type == float:
            return float(value)
        elif hasattr(target_type, '__origin__'):
            # Handle generic types like List[str], Optional[int], etc.
            origin = target_type.__origin__
            
            if origin == Union:
                # Handle Optional[T] (which is Union[T, None])
                args = target_type.__args__
                if len(args) == 2 and type(None) in args:
                    # This is Optional[T]
                    non_none_type = args[0] if args[1] == type(None) else args[1]
                    return convert_value(value, non_none_type)
                else:
                    # Try each type in the union
                    for arg_type in args:
                        try:
                            return convert_value(value, arg_type)
                        except (ValueError, TypeConversionError):
                            continue
                    raise ValueError(f"Cannot convert '{value}' to any type in {target_type}")
            
            elif origin in (list, List):
                # Handle List[T]
                if target_type.__args__:
                    item_type = target_type.__args__[0]
                    # Split by comma and convert each item
                    items = [item.strip() for item in value.split(',')]
                    return [convert_value(item, item_type) for item in items if item]
                else:
                    return value.split(',')
            
            else:
                # For other generic types, try direct conversion
                return target_type(value)
        
        elif hasattr(target_type, '__members__'):  # Enum
            # Handle enum types
            if hasattr(target_type, '_value2member_map_'):
                # Try by value first
                if value in target_type._value2member_map_:
                    return target_type._value2member_map_[value]
            
            # Try by name
            if hasattr(target_type, '_name2value_'):
                if value in target_type._name2value_:
                    return target_type[value]
            
            # Try case-insensitive name match
            for member in target_type:
                if member.name.lower() == value.lower():
                    return member
            
            raise ValueError(f"'{value}' is not a valid {target_type.__name__}")
        
        else:
            # Try direct conversion
            return target_type(value)
    
    except (ValueError, TypeError) as e:
        raise TypeConversionError(f"Cannot convert '{value}' to {target_type.__name__}: {e}")


def format_type_name(type_obj: Type) -> str:
    """Format a type object into a readable string.
    
    Args:
        type_obj: Type object
        
    Returns:
        Formatted type name
    """
    if hasattr(type_obj, '__name__'):
        return type_obj.__name__
    elif hasattr(type_obj, '__origin__'):
        origin = type_obj.__origin__
        if origin == Union:
            args = type_obj.__args__
            if len(args) == 2 and type(None) in args:
                non_none_type = args[0] if args[1] == type(None) else args[1]
                return f"Optional[{format_type_name(non_none_type)}]"
            else:
                arg_names = [format_type_name(arg) for arg in args]
                return f"Union[{', '.join(arg_names)}]"
        elif origin in (list, List):
            if type_obj.__args__:
                item_type = format_type_name(type_obj.__args__[0])
                return f"List[{item_type}]"
            else:
                return "List"
        else:
            return str(type_obj)
    else:
        return str(type_obj)


# Import List for type annotations
try:
    from typing import List
except ImportError:
    List = list