#!/usr/bin/env python3
"""Demo script showing FastShell non-interactive usage."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from example import app


def run_demo():
    """Run demonstration of various commands."""
    print("🚀 FastShell Demo - Non-interactive Mode\n")
    
    # Demo commands
    commands = [
        "hello",
        "hello --name Alice --count 2",
        "hello Bob --uppercase",
        "add 15 27",
        "add 10 20 --verbose",
        "log 'System started' --level info",
        "log 'Debug message' --level debug --timestamp",
        "calc '2 + 3 * 4'",
        "config --list-all",
        "config --key theme --value light",
        "config --key theme",
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"[{i:2d}] Running: {cmd}")
        print("    Output:", end=" ")
        
        # Capture output by temporarily redirecting stdout
        from io import StringIO
        import contextlib
        
        f = StringIO()
        with contextlib.redirect_stdout(f):
            try:
                app.execute_command(cmd)
            except Exception as e:
                print(f"Error: {e}")
        
        output = f.getvalue().strip()
        if output:
            # Indent multi-line output
            lines = output.split('\n')
            for j, line in enumerate(lines):
                if j == 0:
                    print(line)
                else:
                    print(f"           {line}")
        else:
            print("(no output)")
        
        print()  # Empty line for readability
    
    print("\n✨ Demo completed! Try running 'python example.py' for interactive mode.")
    print("\n📚 Available commands:")
    for name, command in sorted(app.commands.items()):
        description = command.description or "No description"
        print(f"  • {name:<12} - {description}")


if __name__ == "__main__":
    run_demo()