#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
I/O utility functions for todo management.
This module handles reading and writing todos to persistent storage.
"""

# Standard library imports
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Union

# Constants
DATA_DIR = Path("data")
TODOS_FILENAME = "todos.json"
TODOS_PATH = DATA_DIR / TODOS_FILENAME

# Configure logging
logger = logging.getLogger(__name__)


def save_todos(todos: List[Dict[str, Any]]) -> None:
    """
    Save todos to a JSON file in the data directory
    
    Args:
        todos: List of todo dictionaries to save
    """
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(exist_ok=True)
    
    # Write todos to file
    try:
        with open(TODOS_PATH, "w") as file_handle:
            json.dump(todos, file_handle, indent=2)


    except IOError as e:
        logger.error(f"Failed to save todos: {e}")
        raise


def load_todos() -> List[Dict[str, Any]]:
    """
    Load todos from JSON file in the data directory
    
    Returns:
        List of todo dictionaries, or empty list if file doesn't exist
    """
    # Check if the todos file exists
    if TODOS_PATH.exists():
        try:
            with open(TODOS_PATH, "r") as file_handle:
                return json.load(file_handle)
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load todos: {e}")
            return []
    else:
        logger.info("No todos file found, returning empty list")
        return []
