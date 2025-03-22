from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from .translate import translate


@dataclass
class CommandInfo:
    name: str
    description: str
    example: str
    func: Callable


class CommandRegistry:
    def __init__(self):
        self.commands: Dict[str, CommandInfo] = {}

    def register(self, name: str, description: str, example: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.commands[name] = CommandInfo(
                name=name, description=description, example=example, func=func
            )
            return func

        return decorator

    def execute(self, command: str, *args: Any) -> str:
        if command not in self.commands:
            return f"Unknown command: {command}"
        return self.commands[command].func(*args)

    def get_commands(self) -> List[CommandInfo]:
        return list(self.commands.values())


registry = CommandRegistry()

# Register commands
registry.register(
    "translate", "Translate text to a target language", '/translate("Hello", "IT")'
)(translate)


def process_command(text: str) -> str:
    if not text.startswith("/"):
        return text

    # Remove the leading slash and split into command and arguments
    command_text = text[1:].strip()
    parts = command_text.split("(", 1)
    if len(parts) != 2:
        return text

    command = parts[0].strip()
    args_text = parts[1].rstrip(")")

    # Parse arguments - this is a simple implementation
    args = [arg.strip().strip('"') for arg in args_text.split(",")]

    return registry.execute(command, *args)
