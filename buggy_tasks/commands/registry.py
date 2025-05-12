"""
Command Registry System

This module provides a registry system for slash commands used in the todo application.
Commands are registered with a name, description, and example, and can be executed
with arguments.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

# Import available command implementations
from .translate import translate


@dataclass(frozen=True)
class CommandInfo:
    """Information about a registered command"""
    name: str
    description: str
    example: str
    func: Callable
    enabled: bool = field(default=True)


class CommandRegistry:
    """
    Registry for slash commands that can be executed in the todo app.
    
    Commands are registered with a decorator and can be executed by name.
    """
    
    def __init__(self):
        """Initialize an empty command registry."""
        # Storage for registered commands
        self.commands: Dict[str, CommandInfo] = {}

    def register(self, name: str, description: str, example: str) -> Callable:
        """
        Decorator that registers a function as a command.
        
        Args:
            name: Command name (without slash)
            description: Human-readable description of what the command does
            example: Example usage of the command
            
        Returns:
            Decorator function that registers the command
        """
        def decorator(func: Callable) -> Callable:
            # Create a CommandInfo object and store it in the registry
            self.commands[name] = CommandInfo(
                name=name,
                description=description,
                example=example,
                func=func
            )
            # Return the original function unchanged
            return func

        return decorator

    def execute(self, command: str, *args: Any) -> str:
        """
        Execute a registered command.
        
        Args:
            command: Command name to execute
            *args: Arguments to pass to the command function
            
        Returns:
            Result of the command execution
        """
        # Check if the command exists
        if command not in self.commands:
            return f"Unknown command: {command}"
            
        # Execute the command with provided arguments
        return self.commands[command].func(*args)

    def get_commands(self) -> List[CommandInfo]:
        """
        Get all registered commands.
        
        Returns:
            List of CommandInfo objects for all registered commands
        """
        # Return a copy of the values to prevent modification
        return list(self.commands.values())


# Create the singleton registry instance for the application
registry = CommandRegistry()

# ============================================================
# Register all available commands below
# ============================================================

# The translate command - converts text to different languages
registry.register(
    name="translate",
    description="Translate text to a target language using AI",
    example='/translate("Learn how to make pasta", "IT")',
)(translate)

# Add more commands here as needed
# registry.register(...)

# ============================================================


def process_command(text: str) -> str:
    """
    Process a text command with slash notation.
    
    Parses commands in the format /command(arg1, arg2, ...) and executes them
    using the command registry.
    
    Args:
        text: The text that may contain a command
        
    Returns:
        The result of the command execution if the text contains a valid command,
        otherwise the original text
    """
    # Quick check if this even looks like a command
    if not text or not text.startswith("/"):
        return text
        
    try:
        # Extract the command portion (after slash, before parenthesis)
        command_text = text[1:].strip()
        
        # Split into command name and arguments part
        command_parts = command_text.split("(", 1)
        
        # Validate format - must have command name and arguments in parentheses
        if len(command_parts) != 2:
            return text  # Not a valid command format
            
        # Extract command name and arguments text
        command_name = command_parts[0].strip()
        arguments_text = command_parts[1].rstrip(")")
        
        # Parse individual arguments
        # This is a simple parser that just splits by commas and removes quotes
        command_args = []
        if arguments_text:
            command_args = [arg.strip().strip('"').strip("'") for arg in arguments_text.split(",")]
            
        # Execute the command with its arguments
        return registry.execute(command_name, *command_args)
        
    except Exception as e:
        # If any error occurs during processing, log it and return the original text
        import logging
        logging.getLogger(__name__).error(f"Error processing command '{text}': {e}")
        return text
