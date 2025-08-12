"""Auto-completion for FastShell."""

from typing import Dict, List, Iterable
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document

from .command import Command
from .parser import CommandParser
from .types import ParameterType


class FastShellCompleter(Completer):
    """Auto-completer for FastShell commands and parameters."""
    
    def __init__(self, commands: Dict[str, Command]):
        """Initialize completer.
        
        Args:
            commands: Dictionary of available commands
        """
        self.commands = commands
        self.parser = CommandParser()
    
    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        """Get completions for the current document.
        
        Args:
            document: Current document
            complete_event: Completion event
            
        Yields:
            Completion objects
        """
        text = document.text_before_cursor
        
        # Parse the current command line
        try:
            parsed = self.parser.parse_partial(text)
        except Exception:
            return
        
        # If no command yet, complete command names
        if not parsed.command or (not text.strip() or not ' ' in text.strip()):
            yield from self._complete_commands(text)
            return
        
        # Complete command parameters
        if parsed.command in self.commands:
            command = self.commands[parsed.command]
            yield from self._complete_parameters(command, parsed, text)
    
    def _complete_commands(self, text: str) -> Iterable[Completion]:
        """Complete command names.
        
        Args:
            text: Current text
            
        Yields:
            Command name completions
        """
        word = text.strip().split()[-1] if text.strip() else ""
        
        for command_name, command in self.commands.items():
            if command_name.startswith(word):
                display_meta = command.description or "No description"
                yield Completion(
                    command_name,
                    start_position=-len(word),
                    display_meta=display_meta
                )
    
    def _complete_parameters(self, command: Command, parsed, text: str) -> Iterable[Completion]:
        """Complete command parameters.
        
        Args:
            command: Command to complete for
            parsed: Parsed command
            text: Current text
            
        Yields:
            Parameter completions
        """
        words = text.strip().split()
        if not words:
            return
        
        current_word = words[-1] if not text.endswith(' ') else ""
        
        # Complete option names
        if current_word.startswith('-'):
            yield from self._complete_option_names(command, current_word)
        else:
            # Check if we're completing a value for an option
            if len(words) >= 2 and words[-2].startswith('-'):
                option_name = words[-2].lstrip('-').replace('-', '_')
                yield from self._complete_option_values(command, option_name, current_word)
            else:
                # Complete positional arguments or suggest options
                yield from self._complete_positional_or_options(command, parsed, current_word)
    
    def _complete_option_names(self, command: Command, current_word: str) -> Iterable[Completion]:
        """Complete option names.
        
        Args:
            command: Command to complete for
            current_word: Current word being typed
            
        Yields:
            Option name completions
        """
        prefix = "--" if current_word.startswith('--') else "-"
        word = current_word.lstrip('-')
        
        for param in command.parameters:
            if param.parameter_type == ParameterType.OPTION:
                option_name = param.name.replace('_', '-')
                
                if option_name.startswith(word):
                    completion_text = f"{prefix}{option_name}"
                    display_meta = param.description or f"{param.type.__name__}"
                    
                    if param.is_flag:
                        display_meta += " (flag)"
                    
                    yield Completion(
                        completion_text,
                        start_position=-len(current_word),
                        display_meta=display_meta
                    )
    
    def _complete_option_values(self, command: Command, option_name: str, current_word: str) -> Iterable[Completion]:
        """Complete option values.
        
        Args:
            command: Command to complete for
            option_name: Option name
            current_word: Current word being typed
            
        Yields:
            Option value completions
        """
        # Find the parameter
        param = None
        for p in command.parameters:
            if p.name == option_name:
                param = p
                break
        
        if not param:
            return
        
        # Provide type-specific completions
        if param.type == bool:
            for value in ['true', 'false']:
                if value.startswith(current_word.lower()):
                    yield Completion(
                        value,
                        start_position=-len(current_word),
                        display_meta="boolean value"
                    )
        elif hasattr(param.type, '__members__'):  # Enum
            for member in param.type.__members__:
                if member.lower().startswith(current_word.lower()):
                    yield Completion(
                        member,
                        start_position=-len(current_word),
                        display_meta=f"enum value"
                    )
    
    def _complete_positional_or_options(self, command: Command, parsed, current_word: str) -> Iterable[Completion]:
        """Complete positional arguments or suggest options.
        
        Args:
            command: Command to complete for
            parsed: Parsed command
            current_word: Current word being typed
            
        Yields:
            Completions for positional args or options
        """
        # Count how many positional arguments we already have
        arg_count = len(parsed.args)
        
        # Find the next expected positional argument
        positional_params = [p for p in command.parameters if p.parameter_type == ParameterType.ARGUMENT]
        
        if arg_count < len(positional_params):
            param = positional_params[arg_count]
            
            # Provide type hint for the expected argument
            if not current_word:
                yield Completion(
                    "",
                    start_position=0,
                    display=f"<{param.name}>",
                    display_meta=f"{param.type.__name__}: {param.description or 'No description'}"
                )
        
        # Also suggest available options that haven't been used
        used_options = set(parsed.kwargs.keys())
        
        for param in command.parameters:
            if param.parameter_type == ParameterType.OPTION and param.name not in used_options:
                option_name = f"--{param.name.replace('_', '-')}"
                if option_name.startswith(current_word) or not current_word:
                    display_meta = param.description or f"{param.type.__name__}"
                    if param.is_flag:
                        display_meta += " (flag)"
                    
                    yield Completion(
                        option_name,
                        start_position=-len(current_word),
                        display_meta=display_meta
                    )