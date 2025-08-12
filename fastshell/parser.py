"""Command line parser for FastShell."""

import shlex
from typing import List, Dict, Optional

from .types import ParsedCommand
from .exceptions import ParseError


class CommandParser:
    """Parses command line input into structured format."""
    
    def parse(self, command_line: str) -> ParsedCommand:
        """Parse a command line string.
        
        Args:
            command_line: Command line to parse
            
        Returns:
            ParsedCommand instance
            
        Raises:
            ParseError: If parsing fails
        """
        try:
            tokens = shlex.split(command_line)
        except ValueError as e:
            raise ParseError(f"Failed to parse command line: {e}")
        
        if not tokens:
            return ParsedCommand()
        
        command = tokens[0]
        args = []
        kwargs = {}
        
        i = 1
        while i < len(tokens):
            token = tokens[i]
            
            if token.startswith('--'):
                # Long option
                option_name = token[2:].replace('-', '_')
                
                if '=' in option_name:
                    # --option=value format
                    option_name, value = option_name.split('=', 1)
                    kwargs[option_name] = value
                else:
                    # --option value format
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                        kwargs[option_name] = tokens[i + 1]
                        i += 1
                    else:
                        # Boolean flag
                        kwargs[option_name] = 'true'
                        
            elif token.startswith('-') and len(token) > 1:
                # Short option
                option_name = token[1:]
                
                if len(option_name) == 1:
                    # Single character option
                    if i + 1 < len(tokens) and not tokens[i + 1].startswith('-'):
                        kwargs[option_name] = tokens[i + 1]
                        i += 1
                    else:
                        # Boolean flag
                        kwargs[option_name] = 'true'
                else:
                    # Multiple character short option or combined flags
                    if '=' in option_name:
                        option_name, value = option_name.split('=', 1)
                        kwargs[option_name] = value
                    else:
                        # Treat as boolean flag
                        kwargs[option_name] = 'true'
            else:
                # Positional argument
                args.append(token)
            
            i += 1
        
        return ParsedCommand(command=command, args=args, kwargs=kwargs)
    
    def parse_partial(self, command_line: str) -> ParsedCommand:
        """Parse a partial command line for completion.
        
        Args:
            command_line: Partial command line
            
        Returns:
            ParsedCommand instance with partial parsing
        """
        try:
            # For partial parsing, we need to handle incomplete tokens
            tokens = []
            current_token = ""
            in_quotes = False
            quote_char = None
            
            i = 0
            while i < len(command_line):
                char = command_line[i]
                
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_token += char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                    current_token += char
                elif char == ' ' and not in_quotes:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                else:
                    current_token += char
                
                i += 1
            
            # Add the last token even if incomplete
            if current_token or command_line.endswith(' '):
                tokens.append(current_token)
            
            if not tokens:
                return ParsedCommand()
            
            command = tokens[0] if tokens[0] else None
            args = []
            kwargs = {}
            
            i = 1
            while i < len(tokens):
                token = tokens[i]
                
                if token.startswith('--'):
                    option_name = token[2:].replace('-', '_')
                    
                    if '=' in option_name:
                        option_name, value = option_name.split('=', 1)
                        kwargs[option_name] = value
                    else:
                        if i + 1 < len(tokens):
                            kwargs[option_name] = tokens[i + 1]
                            i += 1
                        else:
                            kwargs[option_name] = ''
                            
                elif token.startswith('-') and len(token) > 1:
                    option_name = token[1:]
                    
                    if len(option_name) == 1:
                        if i + 1 < len(tokens):
                            kwargs[option_name] = tokens[i + 1]
                            i += 1
                        else:
                            kwargs[option_name] = ''
                    else:
                        if '=' in option_name:
                            option_name, value = option_name.split('=', 1)
                            kwargs[option_name] = value
                        else:
                            kwargs[option_name] = 'true'
                else:
                    args.append(token)
                
                i += 1
            
            return ParsedCommand(command=command, args=args, kwargs=kwargs)
            
        except Exception:
            # Fallback for any parsing errors in partial mode
            return ParsedCommand()