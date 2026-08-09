from argparse import Namespace

import pytest

from src.cli import commands
from src.models import User, Project, Task


@pytest.fixture(autouse=True)
def reset_registries(monkeypatch):
    """Reset registries and stub out disk writes for CLI-level tests."""
    User.reset()
    Project.reset()
    Task.reset()
    monkeypatch.setattr(commands, "save_data", lambda *a, **k: None)
    yield
    User.reset()
    Project.reset()
    Task.reset()


def test_add_user_creates_user():
    commands.add_user(Namespace(name="Alex", email="alex@example.com"))
    assert User.find_by_name("Alex") is not None


def test_add_user_duplicate_is_noop():
    commands.add_user(Namespace(name="Alex", email="alex@example.com"))
    commands.add_user(Namespace(name="Alex", email="other@example.com"))
    assert len(User.all()) == 1


def test_add_project_requires_existing_user():
    commands.add_project(
        Namespace(user="Ghost", title="X", description="", due_date=None)
    )
    assert Project.all() == []


def test_add_project_success():
    commands.add_user(Namespace(name="Alex", email="alex@example.com"))
    commands.add_project(
        Namespace(user="Alex", title="CLI Tool", description="desc", due_date="2026-09-01")
    )
    project = Project.find_by_title("CLI Tool")
    assert project is not None
    owner = User.find_by_name("Alex")
    assert project.project_id in owner.project_ids


def test_add_project_rejects_bad_due_date():
    commands.add_user(Namespace(name="Alex", email="alex@example.com"))
    commands.add_project(
        Namespace(user="Alex", title="CLI Tool", description="", due_date="not-a-date")
    )
    assert Project.find_by_title("CLI Tool") is None


def test_add_task_and_complete_task():
    commands.add_user(Namespace(name="Alex", email="alex@example.com"))
    commands.add_project(
        Namespace(user="Alex", title="CLI Tool", description="", due_date=None)
    )
    commands.add_task(
        Namespace(project="CLI Tool", title="Do the thing", assigned_to="Alex")
    )
    task = Task.all()[0]
    assert task.status == "pending"

    commands.complete_task(Namespace(task_id=task.task_id))
    assert task.status == "complete"


def test_complete_task_missing_id_is_noop():
    commands.complete_task(Namespace(task_id=999))
    # No exception raised, nothing to assert on state change.
