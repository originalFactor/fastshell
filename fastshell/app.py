"""FastShell main application class."""

import sys
from typing import Dict, Any, Callable, Optional, List
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from rich.console import Console

from .parser import CommandParser
from .completer import FastShellCompleter
from .command import Command
from .exceptions import FastShellException, CommandNotFound
from .validation import ValidationConfig, set_validation_config
from .formatter import OutputFormat, create_formatter


class FastShell:
    """Main FastShell application class."""

    def __init__(
        self,
        name: str = "fastshell",
        description: str = "",
        use_pydantic: bool = True,
        output_format: str = "auto",
    ):
        """Initialize FastShell application.

        Args:
            name: Application name
            description: Application description
            use_pydantic: Whether to use Pydantic for type validation
            output_format: Default output format for command results
        """
        self.name = name
        self.description = description
        self.use_pydantic = use_pydantic
        self.commands: Dict[str, Command] = {}
        self.console = Console()
        self.parser = CommandParser()
        self.session: Optional[PromptSession] = None
        self.formatter = create_formatter(self.console, output_format)

        # Configure global validation
        validation_config = ValidationConfig(use_pydantic=use_pydantic)
        set_validation_config(validation_config)

    def command(self, name: Optional[str] = None, **kwargs):
        """Decorator to register a command.

        Args:
            name: Command name (defaults to function name)
            **kwargs: Additional command options
        """

        def decorator(func: Callable) -> Callable:
            self.add_command(
                Command.from_function(
                    func,
                    name or func.__name__,
                    use_pydantic=self.use_pydantic,
                    **kwargs,
                )
            )
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

    def execute_command(self, command_line: str, format_output: bool = True) -> Any:
        """Execute a command from command line string.

        Args:
            command_line: Command line to execute
            format_output: Whether to format and display the output

        Returns:
            Command execution result
        """
        try:
            parsed = self.parser.parse(command_line)
            if not parsed.command:
                return

            # Handle built-in help command
            if parsed.command.lower() == "help":
                self._show_help()
                return

            command = self.get_command(parsed.command)
            result = command.execute(parsed.args, parsed.kwargs)

            # Format and display result if requested
            if format_output and result is not None:
                self.formatter.format_result(result)

            return result

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

                if command_line.lower() in ["exit", "quit"]:
                    break

                if command_line.lower() == "help":
                    self._show_help()
                    continue

                # Handle built-in format command
                if command_line.lower().startswith("format "):
                    format_type = command_line[7:].strip()
                    if format_type in self.get_available_formats():
                        self.set_output_format(format_type)
                    else:
                        self.console.print(f"[red]Invalid format: {format_type}[/red]")
                        self.console.print(
                            f"[dim]Available formats: {', '.join(self.get_available_formats())}[/dim]"
                        )
                    continue

                if command_line.lower() == "format":
                    self.console.print(
                        f"[cyan]Current format: {self.formatter.default_format.value}[/cyan]"
                    )
                    self.console.print(
                        f"[dim]Available formats: {', '.join(self.get_available_formats())}[/dim]"
                    )
                    self.console.print("[dim]Usage: format <type>[/dim]")
                    continue

                self.execute_command(command_line)

            except KeyboardInterrupt:
                continue
            except EOFError:
                break

        self.console.print("\n[dim]Goodbye![/dim]")

    def set_output_format(self, format_type: str) -> None:
        """Set the output format for command results.

        Args:
            format_type: Output format (auto, json, table, tree, plain, pretty)
        """
        self.formatter = create_formatter(self.console, format_type)
        self.console.print(f"[green]Output format set to: {format_type}[/green]")

    def get_available_formats(self) -> List[str]:
        """Get list of available output formats.

        Returns:
            List of format names
        """
        return [fmt.value for fmt in OutputFormat]

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

        self.console.print(
            "\n[dim]Use '<command> --help' for detailed command help.[/dim]"
        )
        self.console.print(
            f"\n[dim]Current output format: {self.formatter.default_format.value}[/dim]"
        )
        self.console.print(
            f"[dim]Available formats: {', '.join(self.get_available_formats())}[/dim]"
        )
        self.console.print("[dim]Use 'format <type>' to change output format.[/dim]")
