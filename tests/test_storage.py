import json

import pytest

from src.models import User, Project, Task
from src.utils.storage import save_data, load_data


@pytest.fixture(autouse=True)
def reset_registries():
    User.reset()
    Project.reset()
    Task.reset()
    yield
    User.reset()
    Project.reset()
    Task.reset()


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "data.json"

    alex = User(name="Alex", email="alex@example.com")
    project = Project(title="CLI Tool", owner_id=alex.user_id)
    alex.add_project(project)
    task = Task(title="Implement add-task", project_id=None, assigned_to="Alex")
    project.add_task(task)

    save_data(path=str(path))

    User.reset()
    Project.reset()
    Task.reset()
    load_data(path=str(path))

    assert len(User.all()) == 1
    assert User.all()[0].name == "Alex"
    assert len(Project.all()) == 1
    assert Project.all()[0].title == "CLI Tool"
    assert len(Task.all()) == 1
    assert Task.all()[0].status == "pending"


def test_load_data_missing_file_is_empty(tmp_path):
    path = tmp_path / "missing.json"
    load_data(path=str(path))
    assert User.all() == []
    assert Project.all() == []
    assert Task.all() == []


def test_load_data_malformed_json_is_empty(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{not valid json")
    load_data(path=str(path))
    assert User.all() == []
