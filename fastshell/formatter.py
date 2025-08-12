"""Output formatting for FastShell command results."""

import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, date
from enum import Enum
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax
from rich.pretty import Pretty


class OutputFormat(Enum):
    """Available output formats."""
    AUTO = "auto"
    JSON = "json"
    TABLE = "table"
    TREE = "tree"
    PLAIN = "plain"
    PRETTY = "pretty"


class ResultFormatter:
    """Formats command execution results for display."""
    
    def __init__(self, console: Console, default_format: OutputFormat = OutputFormat.AUTO):
        """Initialize formatter.
        
        Args:
            console: Rich console instance
            default_format: Default output format
        """
        self.console = console
        self.default_format = default_format
    
    def format_result(self, result: Any, format_type: Optional[OutputFormat] = None) -> None:
        """Format and display command result.
        
        Args:
            result: Command execution result
            format_type: Specific format to use (overrides default)
        """
        if result is None:
            return
        
        format_to_use = format_type or self.default_format
        
        # Auto-detect best format if AUTO is selected
        if format_to_use == OutputFormat.AUTO:
            format_to_use = self._detect_best_format(result)
        
        # Format based on type
        if format_to_use == OutputFormat.JSON:
            self._format_json(result)
        elif format_to_use == OutputFormat.TABLE:
            self._format_table(result)
        elif format_to_use == OutputFormat.TREE:
            self._format_tree(result)
        elif format_to_use == OutputFormat.PLAIN:
            self._format_plain(result)
        elif format_to_use == OutputFormat.PRETTY:
            self._format_pretty(result)
        else:
            self._format_auto(result)
    
    def _detect_best_format(self, result: Any) -> OutputFormat:
        """Detect the best format for the given result.
        
        Args:
            result: Result to analyze
            
        Returns:
            Best format for the result
        """
        if isinstance(result, (dict, list)):
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                # List of dictionaries - good for table
                return OutputFormat.TABLE
            elif isinstance(result, dict) and len(result) > 3:
                # Large dictionary - good for tree
                return OutputFormat.TREE
            else:
                # Small dict or list - use pretty
                return OutputFormat.PRETTY
        elif isinstance(result, str) and (result.startswith('{') or result.startswith('[')):
            # Looks like JSON string
            return OutputFormat.JSON
        else:
            # Simple values
            return OutputFormat.PLAIN
    
    def _format_json(self, result: Any) -> None:
        """Format result as JSON."""
        try:
            if isinstance(result, str):
                # Try to parse if it's a JSON string
                parsed = json.loads(result)
                json_str = json.dumps(parsed, indent=2, ensure_ascii=False, default=str)
            else:
                json_str = json.dumps(result, indent=2, ensure_ascii=False, default=str)
            
            syntax = Syntax(json_str, "json", theme="monokai", line_numbers=True)
            self.console.print(Panel(syntax, title="[bold blue]JSON Output[/bold blue]", border_style="blue"))
        except (json.JSONDecodeError, TypeError):
            # Fallback to pretty format
            self._format_pretty(result)
    
    def _format_table(self, result: Any) -> None:
        """Format result as table."""
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], dict):
                # List of dictionaries
                table = Table(title="Command Result", show_header=True, header_style="bold magenta")
                
                # Add columns from first item
                for key in result[0].keys():
                    table.add_column(str(key), style="cyan")
                
                # Add rows
                for item in result:
                    row = [str(item.get(key, "")) for key in result[0].keys()]
                    table.add_row(*row)
                
                self.console.print(table)
            else:
                # List of simple values
                table = Table(title="Command Result", show_header=True, header_style="bold magenta")
                table.add_column("Index", style="dim")
                table.add_column("Value", style="cyan")
                
                for i, item in enumerate(result):
                    table.add_row(str(i), str(item))
                
                self.console.print(table)
        elif isinstance(result, dict):
            # Dictionary as table
            table = Table(title="Command Result", show_header=True, header_style="bold magenta")
            table.add_column("Key", style="bold cyan")
            table.add_column("Value", style="green")
            
            for key, value in result.items():
                table.add_row(str(key), str(value))
            
            self.console.print(table)
        else:
            # Fallback to pretty format
            self._format_pretty(result)
    
    def _format_tree(self, result: Any) -> None:
        """Format result as tree structure."""
        tree = Tree("[bold blue]Command Result[/bold blue]")
        self._add_to_tree(tree, result)
        self.console.print(tree)
    
    def _add_to_tree(self, parent: Tree, obj: Any, key: str = None) -> None:
        """Recursively add objects to tree.
        
        Args:
            parent: Parent tree node
            obj: Object to add
            key: Key name for the object
        """
        if isinstance(obj, dict):
            if key:
                node = parent.add(f"[bold cyan]{key}[/bold cyan] (dict)")
            else:
                node = parent
            
            for k, v in obj.items():
                self._add_to_tree(node, v, str(k))
        
        elif isinstance(obj, list):
            if key:
                node = parent.add(f"[bold cyan]{key}[/bold cyan] (list[{len(obj)}])")
            else:
                node = parent
            
            for i, item in enumerate(obj):
                self._add_to_tree(node, item, f"[{i}]")
        
        else:
            value_str = str(obj)
            if len(value_str) > 50:
                value_str = value_str[:47] + "..."
            
            if key:
                parent.add(f"[cyan]{key}[/cyan]: [green]{value_str}[/green]")
            else:
                parent.add(f"[green]{value_str}[/green]")
    
    def _format_plain(self, result: Any) -> None:
        """Format result as plain text."""
        if isinstance(result, str):
            self.console.print(result)
        else:
            self.console.print(str(result))
    
    def _format_pretty(self, result: Any) -> None:
        """Format result using Rich's pretty printer."""
        self.console.print(Pretty(result, expand_all=True))
    
    def _format_auto(self, result: Any) -> None:
        """Auto-format result with enhanced styling."""
        if result is None:
            return
        
        # Add timestamp and type info
        timestamp = datetime.now().strftime("%H:%M:%S")
        result_type = type(result).__name__
        
        # Create header
        header = f"[dim]{timestamp}[/dim] [bold green]✓[/bold green] [cyan]{result_type}[/cyan]"
        
        if isinstance(result, (str, int, float, bool)):
            # Simple values with styling
            if isinstance(result, bool):
                value_color = "green" if result else "red"
                self.console.print(f"{header}: [{value_color}]{result}[/{value_color}]")
            elif isinstance(result, (int, float)):
                self.console.print(f"{header}: [yellow]{result}[/yellow]")
            else:
                self.console.print(f"{header}: [white]{result}[/white]")
        
        elif isinstance(result, (list, tuple)):
            # Lists and tuples
            if len(result) == 0:
                self.console.print(f"{header}: [dim]empty[/dim]")
            elif len(result) <= 5:
                # Small lists - show inline
                items = ", ".join([f"[green]{item}[/green]" for item in result])
                self.console.print(f"{header}: [{items}]")
            else:
                # Large lists - show summary
                self.console.print(f"{header}: [dim]{len(result)} items[/dim]")
                self._format_pretty(result)
        
        elif isinstance(result, dict):
            # Dictionaries
            if len(result) == 0:
                self.console.print(f"{header}: [dim]empty[/dim]")
            elif len(result) <= 3:
                # Small dicts - show inline
                items = ", ".join([f"[cyan]{k}[/cyan]: [green]{v}[/green]" for k, v in result.items()])
                self.console.print(f"{header}: {{{items}}}")
            else:
                # Large dicts - show summary and details
                self.console.print(f"{header}: [dim]{len(result)} keys[/dim]")
                self._format_pretty(result)
        
        else:
            # Complex objects
            self.console.print(f"{header}:")
            self._format_pretty(result)


def create_formatter(console: Console, format_type: str = "auto") -> ResultFormatter:
    """Create a result formatter.
    
    Args:
        console: Rich console instance
        format_type: Output format type
        
    Returns:
        ResultFormatter instance
    """
    try:
        output_format = OutputFormat(format_type.lower())
    except ValueError:
        output_format = OutputFormat.AUTO
    
    return ResultFormatter(console, output_format)