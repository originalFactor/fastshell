"""FastShell main application class."""

import sys
from typing import Dict, Any, Callable, Optional, List
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console
from rich.text import Text

from .parser import CommandParser
from .completer import FastShellCompleter
from .command import Command
from .exceptions import FastShellException, CommandNotFound, InvalidArguments


class FastShell:
    """Main FastShell application class."""
    
    def __init__(self, name: str = "fastshell", description: str = ""):
        """Initialize FastShell application.
        
        Args:
            name: Application name
            description: Application description
        """
        self.name = name
        self.description = description
        self.commands: Dict[str, Command] = {}
        self.console = Console()
        self.parser = CommandParser()
        self.session: Optional[PromptSession] = None
        
    def command(self, name: Optional[str] = None, **kwargs):
        """Decorator to register a command.
        
        Args:
            name: Command name (defaults to function name)
            **kwargs: Additional command options
        """
        def decorator(func: Callable) -> Callable:
            cmd_name = name or func.__name__
            command = Command.from_function(func, cmd_name, **kwargs)
            self.commands[cmd_name] = command
            return func
        return decorator
    
    def add_command(self, command: Command):
        """Add a command to the application.
        
        Args:
            command: Command instance to add
        """
        self.commands[command.name] = command
    
    def get_command(self, name: str) -> Command:
        """Get a command by name.
        
        Args:
            name: Command name
            
        Returns:
            Command instance
            
        Raises:
            CommandNotFound: If command doesn't exist
        """
        if name not in self.commands:
            raise CommandNotFound(f"Command '{name}' not found")
        return self.commands[name]
    
    def execute_command(self, command_line: str) -> Any:
        """Execute a command from command line string.
        
        Args:
            command_line: Command line to execute
            
        Returns:
            Command execution result
        """
        try:
            parsed = self.parser.parse(command_line)
            if not parsed.command:
                return
                
            command = self.get_command(parsed.command)
            return command.execute(parsed.args, parsed.kwargs)
            
        except FastShellException as e:
            self.console.print(f"[red]Error: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]Unexpected error: {e}[/red]")
    
    def run_interactive(self):
        """Run the application in interactive mode."""
        completer = FastShellCompleter(self.commands)
        history = InMemoryHistory()
        
        self.session = PromptSession(
            completer=completer,
            history=history,
            complete_while_typing=True,
        )
        
        self.console.print(f"[bold blue]{self.name}[/bold blue]")
        if self.description:
            self.console.print(f"[dim]{self.description}[/dim]")
        self.console.print("Type 'help' for available commands or 'exit' to quit.\n")
        
        while True:
            try:
                command_line = self.session.prompt(f"{self.name}> ")
                command_line = command_line.strip()
                
                if not command_line:
                    continue
                    
                if command_line.lower() in ['exit', 'quit']:
                    break
                    
                if command_line.lower() == 'help':
                    self._show_help()
                    continue
                    
                self.execute_command(command_line)
                
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
        
        self.console.print("\n[dim]Goodbye![/dim]")
    
    def run(self, args: Optional[List[str]] = None):
        """Run the application.
        
        Args:
            args: Command line arguments (defaults to sys.argv[1:])
        """
        if args is None:
            args = sys.argv[1:]
            
        if not args:
            self.run_interactive()
        else:
            command_line = " ".join(args)
            self.execute_command(command_line)
    
    def _show_help(self):
        """Show help information."""
        self.console.print("[bold]Available commands:[/bold]\n")
        
        for name, command in sorted(self.commands.items()):
            description = command.description or "No description available"
            self.console.print(f"  [cyan]{name}[/cyan] - {description}")
        
        self.console.print("\n[dim]Use '<command> --help' for detailed command help.[/dim]")