"""JSON file persistence for users, projects, and tasks."""

import json
import os

from src.models import User, Project, Task

DEFAULT_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "data.json",
)


def load_data(path=DEFAULT_DATA_PATH):
    """Load users/projects/tasks from disk into the model registries.

    Missing or malformed files are treated as an empty dataset rather
    than crashing the CLI.
    """
    User.reset()
    Project.reset()
    Task.reset()

    if not os.path.exists(path):
        return

    try:
        with open(path, "r") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, OSError):
        return

    for user_data in raw.get("users", []):
        User.from_dict(user_data)
    for project_data in raw.get("projects", []):
        Project.from_dict(project_data)
    for task_data in raw.get("tasks", []):
        Task.from_dict(task_data)


def save_data(path=DEFAULT_DATA_PATH):
    """Persist the current in-memory registries to disk as JSON."""
    payload = {
        "users": [u.to_dict() for u in User.all()],
        "projects": [p.to_dict() for p in Project.all()],
        "tasks": [t.to_dict() for t in Task.all()],
    }
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
