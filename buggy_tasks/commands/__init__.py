"""
Command System Package

This package provides the slash command functionality for the Buggy Tasks application.
"""

# Re-export the command registry and processing function
from buggy_tasks.commands.registry import process_command, registry

# Version information
__version__ = '0.1.0'
