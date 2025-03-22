import json
from pathlib import Path


def save_todos(todos):
    """Save todos to a JSON file in the data directory"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    with open(data_dir / "todos.json", "w") as f:
        json.dump(todos, f)


def load_todos():
    """Load todos from JSON file in the data directory"""
    data_dir = Path("data")
    if (data_dir / "todos.json").exists():
        with open(data_dir / "todos.json", "r") as f:
            return json.load(f)
    return []
